# 🛡️ CipherMind: Unified Intelligence Matrix

🚀 **Live Deployment:** [Access CipherMind Here](https://ciphermind.onrender.com)

An AI-powered Retrieval-Augmented Generation (RAG) engine designed to securely ingest, vectorize, and query document knowledge bases.

# CipherMind 🧠🔒

CipherMind is a production-ready, multi-modal Retrieval-Augmented Generation (RAG) platform designed to bridge the gap between AI automation and professional security engineering. Built entirely with a high-resilience FastAPI backend, the system architecture utilizes a dynamically cascading API pool to eliminate rate limits while offering isolated operational domains for general tasks and advanced adversarial security analysis.

---

## ✨ Key Features

### 🛡️ Dual-Domain Intelligence Matrix
* **General Mode:** Designed for standard administrative, architectural, and educational document processing. Optimized for technical guides, corporate policy compliance check-ups, and automated formatting.
* **Cyber Mode:** A hardened adversarial threat-hunting interface. Forces the LLM engine into a strict security-auditing persona that actively hunts for threat vectors, evaluates attack surfaces, and provides production-grade remediation code.

### 🏗️ Advanced Architectural Achievements
* **The Head & Tail Stapler RAG Engine:** A custom context optimization algorithm built to bypass long-document dilution. When parsing heavy log dumps, the engine isolates structural patterns and anomalies at both boundaries of the document window, effortlessly identifying needle-in-a-haystack exploits.
* **Contextual Session Isolation:** Data privacy by design. Session structures are isolated natively via unique frontend-generated tracking tokens, ensuring zero data cross-contamination between users. 
* **Infinite Scaling:** Implements a dynamic fallback loop cascading across multiple API models (Llama-3, Qwen), maintaining high server uptime and structural parsing resilience under heavy loads.

---

## 🛠️ Verified Test Scenarios

CipherMind has successfully passed a rigorous, adversarial quality assurance matrix:

1. **Static Vulnerability Code Auditing:** Parsed insecure PHP login scripts, flagged SQL Injection vectors, detailed exploit mechanics, and wrote secure parameterized query refactors.
2. **API Intruder Payload Analysis:** Detected hidden API manipulation attempts within complex JSON bodies, flagging Privilege Escalation attempts.
3. **Heavy Log Traversal Hunting:** Chewed through highly inflated server logs using the Stapler algorithm to capture a single isolated Path Traversal payload (`../../../etc/passwd`).
4. **Semantic Middle-Search Extraction:** Leveraged a ChromaDB vector implementation to bypass extensive filler text and accurately isolate rules hidden in the exact geometric center of a document.

---

## 🚀 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/shriyashakhil4/CipherMind.git](https://github.com/shriyashakhil4/CipherMind.git)
cd CipherMind

---

## Quick Start (One-Click Launcher)

Requires **Python 3.10+** installed on your machine, and free API keys from
[Groq](https://console.groq.com) and [Hugging Face](https://huggingface.co/settings/tokens).

1. Unzip the project.
2. **Windows:** double-click `start_windows.bat`
   **Mac / Linux:** double-click `start_mac_linux.command` (if it opens as text instead of running, right-click → Open, or run `chmod +x start_mac_linux.command` once in a terminal)
3. On first run it creates a `.env` file for you — open it and paste in your `HF_API_TOKEN` and `GROQ_API_KEY_1`, then continue.
4. The script installs dependencies and starts the server automatically, opening `http://127.0.0.1:8000` in your browser.

Every run after the first is fast — it reuses the same virtual environment.
