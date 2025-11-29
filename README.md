# AI-Agent

Voice-enabled conversational assistant combining LLM conversational power with speech (STT/TTS) and retrieval-augmented answers (RAG).

## Quickstart (developer)

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend (placeholder)
Open `frontend/README.md` for frontend instructions.

## Repo contents
- backend/: FastAPI backend (STT, LLM gateway, RAG hooks)
- frontend/: frontend placeholder (React / mobile)
- README.md
- LICENSE (MIT)

## License
MIT
