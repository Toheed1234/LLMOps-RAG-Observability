# Local LLMOps RAG Assistant 🤖

An enterprise-grade, privacy-focused Retrieval-Augmented Generation (RAG) system running entirely locally. This project answers questions based on personal documents without ever sending data to the cloud, making it fully compliant for enterprise PII handling.

## 📸 Architecture in Action

### 1. Robust Prompt Guardrails
The LangChain system prompts are specifically tuned to absolutely prevent hallucination and mitigate prompt injection attacks (like jailbreaks) while gracefully refusing off-topic requests.
![Streamlit UI](assets/ui_screenshot.png)

### 2. Deep Observability
Configured with **Arize Phoenix** to monitor OpenTelemetry traces, evaluate system latency (TTFT), and track token usage for production-level MLOps readiness.
![Phoenix Dashboard](assets/phoenix_dashboard.png)

## 🏗️ Technical Architecture
- **Inference Engine:** LM Studio (Running massive LLMs entirely locally via llama.cpp bounds)
- **Vector Database:** ChromaDB (Persistent Local Storage)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Lightning-fast CPU embeddings)
- **Orchestration:** LangChain Expression Language (LCEL)
- **Frontend:** Streamlit with dynamic streaming UI
- **Observability:** Arize Phoenix (OpenInference / pyOTel)

## 🛡️ Security & Enterprise Features
- **Strict Guardrails:** Output formatting that rigidly confines the AI from hallucinating or 'leaking' its internal chain-of-thought process.
- **Conversational Memory:** Preserves seamless follow-up capabilities using rolling session state variables without overflowing the model's `n_ctx` limit.
- **Microservice Ready:** Completely containerized with a highly cached `Dockerfile` and a tuned `.dockerignore` to block local virtual environments and databases from bloating the image.
- **Air-gapped Privacy:** 0% Cloud connectivity. Inference, Embeddings, and Databases execute 100% locally.

## 🚀 Run Locally

### 1. Ingest Data
Place any `.pdf` or `.txt` files into the `data/` folder, then build your local Vector Database:
```bash
python src/ingestion.py
```

### 2. Start the App
Boot up the Streamlit UI (which will automatically initialize the Arize Phoenix tracing server):
```bash
streamlit run src/bot.py
```

*Note: You must have an active local inference server (like LM Studio) running on port 1234.*
