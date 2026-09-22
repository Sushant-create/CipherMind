import os
import time
import requests
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

# ---------------------------------------------------------
# 1. LIGHTWEIGHT HUGGING FACE API EMBEDDER 
# ---------------------------------------------------------
class HuggingFaceAPIEmbedder(EmbeddingFunction):
    def __init__(self):
        self.api_token = os.getenv("HF_API_TOKEN")
        self.api_url = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
        
        if not self.api_token:
            print("[WARNING] HF_API_TOKEN not found in environment variables.")

    def __call__(self, input: Documents = None, texts: Documents = None) -> Embeddings:
        docs = input if input is not None else texts
        
        headers = {"Authorization": f"Bearer {self.api_token}"}
        max_retries = 5
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, headers=headers, json={"inputs": docs})
                
                if response.status_code == 200:
                    return response.json()
                
                if response.status_code == 503:
                    try:
                        error_data = response.json()
                        if "loading" in error_data.get("error", "").lower():
                            wait_time = error_data.get("estimated_time", 20.0)
                            print(f"\n[HF INFRASTRUCTURE] Model is waking up on Hugging Face servers...")
                            print(f"[HF INFRASTRUCTURE] Waiting {wait_time} seconds for the GPU to initialize...")
                            time.sleep(wait_time)
                            continue
                    except Exception:
                        pass
                    # 503 but not a "loading" message — retry with backoff
                    last_error = f"HF API 503 Service Unavailable: {response.text}"
                    if attempt < max_retries - 1:
                        print(f"[HF INFRASTRUCTURE] Service unavailable. Retrying in 5 seconds... (Attempt {attempt + 1})")
                        time.sleep(5)
                        continue
                
                # Non-retryable HTTP errors (401, 400, 422, etc.) — fail immediately
                raise Exception(f"HF API Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    print(f"[NETWORK GLITCH] Connection failed. Retrying in 3 seconds... (Attempt {attempt + 1})")
                    time.sleep(3)
                else:
                    raise Exception(f"Critical Failure: Could not reach Hugging Face after {max_retries} attempts. Details: {e}")
        
        # Safety net: if the loop exits without returning or raising
        raise Exception(f"HF Embedding failed after {max_retries} attempts. Last error: {last_error}")

hf_embedder = HuggingFaceAPIEmbedder()


# ---------------------------------------------------------
# 2. CHROMADB VECTOR DATABASE SETUP
# ---------------------------------------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_data")

collections = {
    "general": chroma_client.get_or_create_collection(
        name="general_matrix", 
        embedding_function=hf_embedder
    ),
    "cybersecurity": chroma_client.get_or_create_collection(
        name="cyber_matrix", 
        embedding_function=hf_embedder
    )
}

SESSION_MEMORY = {}


# ---------------------------------------------------------
# 3. THE "HEAD & TAIL STAPLER" CHUNKING ALGORITHM
# ---------------------------------------------------------
def head_and_tail_stapler(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
        
    return chunks


# ---------------------------------------------------------
# 4. DATABASE INGESTION & QUERY FUNCTIONS
# ---------------------------------------------------------
def rebuild_vector_store(domain: str):
    folder_path = f"knowledge_base/system_files/{domain}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        
    collection = collections[domain]

    # FIX: "rebuild" previously never cleared old entries, so re-running this
    # (which happens on every file upload) re-inserted every previously
    # ingested file with the same deterministic IDs -> duplicate-ID errors /
    # stale embeddings. Wipe the collection's contents first so this is a
    # true rebuild.
    existing = collection.get(include=[])
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # FIX: previously only ".txt" files were ingested, silently skipping the
    # shipped ".md" knowledge-base seed files. Accept both.
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    
                chunks = head_and_tail_stapler(content)
                
                ids = [f"{filename}_{i}" for i in range(len(chunks))]
                metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
                
                collection.add(
                    documents=chunks,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Successfully vectorized and stored {filename} in {domain} matrix.")
            except Exception as e:
                print(f"[WARNING] Failed to ingest {filename}: {e}. Skipping this file.")


def query_rag(user_message: str, domain: str, session_id: str) -> str:
    collection = collections[domain]
    
    retrieved_context = ""
    try:
        results = collection.query(
            query_texts=[user_message],
            n_results=3 
        )
        
        if results['documents'] and len(results['documents'][0]) > 0:
            retrieved_context = "\n".join(results['documents'][0])
    except Exception as e:
        # Empty collection or query failure — proceed without context
        print(f"[RAG QUERY] No context retrieved for domain '{domain}': {e}")
        retrieved_context = ""

    if session_id not in SESSION_MEMORY or not isinstance(SESSION_MEMORY[session_id], list):
        SESSION_MEMORY[session_id] = []
        
    SESSION_MEMORY[session_id].append({"role": "user", "content": user_message})
    
    if len(SESSION_MEMORY[session_id]) > 10:
        SESSION_MEMORY[session_id] = SESSION_MEMORY[session_id][-10:]
        
    system_prompt = f"""You are the CipherMind Intelligence Matrix. 
You are currently operating in the {domain.upper()} domain.

Use the following retrieved context to answer the user's query. 
If the context does not contain the answer, rely on your base knowledge, but prioritize the context.

RETRIEVED CONTEXT:
{retrieved_context}
"""

    api_messages = [{"role": "system", "content": system_prompt}]
    api_messages.extend(SESSION_MEMORY[session_id])

    groq_keys = [os.getenv("GROQ_API_KEY_1"), os.getenv("GROQ_API_KEY_2"), os.getenv("GROQ_API_KEY_3")]
    
    for key in groq_keys:
        if not key:
            continue
            
        try:
            groq_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "llama-3.1-8b-instant", 
                    "messages": api_messages,
                    "temperature": 0.3
                }
            )
            
            if groq_response.status_code == 200:
                ai_reply = groq_response.json()["choices"][0]["message"]["content"]
                SESSION_MEMORY[session_id].append({"role": "assistant", "content": ai_reply})
                return ai_reply
            else:
                # --- NEW DIAGNOSTIC LOGGING ---
                print(f"\n[GROQ API REJECTED] Status Code: {groq_response.status_code}")
                print(f"[GROQ ERROR DETAILS]: {groq_response.text}\n")
                
        except Exception as e:
            print(f"Groq Request Failed: {e}. Attempting fallback key...")
            
    return "[SYSTEM ERROR] All Groq API fallbacks failed or rate limit exceeded. Check VS Code terminal."