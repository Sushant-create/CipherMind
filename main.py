import os
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
from rag_engine import query_rag, rebuild_vector_store, SESSION_MEMORY
from document_parser import extract_text_from_file

app = FastAPI(title="CipherMind RAG API")

# NOTE: allow_credentials=True is incompatible with allow_origins=["*"] per the
# CORS spec (browsers reject wildcard origins when credentials are allowed).
# This app doesn't use cookies/auth headers for CORS, so credentials are disabled.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    domain: str
    session_id: Optional[str] = None

# Ensure required directories exist on startup
for domain in ["cybersecurity", "general"]:
    os.makedirs(f"knowledge_base/system_files/{domain}", exist_ok=True)
os.makedirs("temp_processing", exist_ok=True)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.post("/api/init-db")
async def initialize_database():
    try:
        rebuild_vector_store("cybersecurity")
        rebuild_vector_store("general")
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        if request.domain not in ["cybersecurity", "general"]:
            return {"response": "[SYSTEM ERROR: Invalid domain.]"}

        active_session = request.session_id if request.session_id else "default_session"
        response_text = query_rag(request.message, request.domain, active_session)
        return {"response": response_text}
    except Exception as e:
        return {"response": f"**[BACKEND ROUTING ERROR]**: `{str(e)}`"}

@app.post("/api/chat_with_file")
async def chat_with_file_endpoint(
    file: UploadFile = File(...),
    domain: str = Form(...),
    message: str = Form(""),
    session_id: str = Form("")
):
    try:
        if domain not in ["cybersecurity", "general"]:
            return {"response": "[SYSTEM ERROR: Invalid domain.]"}

        active_session = session_id if session_id else "default_session"

        # 1. Save the uploaded file temporarily
        # Sanitize filename to prevent path traversal attacks
        safe_upload_name = os.path.basename(file.filename)
        if not safe_upload_name:
            safe_upload_name = "uploaded_file"
        file_path = f"temp_processing/{safe_upload_name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Extract text using the universal parser (handles pdf, docx, xlsx,
        #    pptx, images via OCR, plain text, and a safe binary fallback for
        #    anything else) instead of only supporting PDF/plain-text.
        try:
            extracted_text = extract_text_from_file(file_path)
        finally:
            # Clean up the temp file to prevent disk space leaks and
            # avoid leaving sensitive uploads on disk
            try:
                os.remove(file_path)
            except OSError:
                pass

        # 3. Save extracted text to the correct domain's knowledge base.
        # Swap ONLY the final extension (not a naive substring replace, which
        # could mangle filenames like "2024.pdf.report.pdf") so every uploaded
        # file lands in the knowledge base as a proper .txt file and is picked
        # up by rebuild_vector_store's ingestion loop.
        base_name = os.path.splitext(safe_upload_name)[0]
        safe_filename = f"{base_name}.txt"
        kb_path = f"knowledge_base/system_files/{domain}/{safe_filename}"
        with open(kb_path, "w", encoding="utf-8") as kb_file:
            kb_file.write(extracted_text)

        # 4. Trigger Vector DB rebuild to ingest the new file
        rebuild_vector_store(domain)

        # 5. Query the matrix (Provide default prompt if user only attached file)
        final_message = message if message.strip() else f"Analyze the recently uploaded document named {file.filename}."
        response_text = query_rag(final_message, domain, active_session)

        return {"response": response_text}

    except Exception as e:
        return {"response": f"**[PIPELINE EXCEPTION]**: `{str(e)}`"}

@app.post("/api/clear-session")
async def clear_session_endpoint(session_id: str = Form(...)):
    # Safely wipe memory without converting it to a string type
    if session_id in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = [] 
    return {"status": "success"}