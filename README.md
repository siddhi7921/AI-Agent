🤖 AI-Agent

A voice-enabled conversational assistant combining the power of LLMs, Speech-to-Text (STT), Text-to-Speech (TTS), and Retrieval-Augmented Generation (RAG).

This project offers a modular architecture with a FastAPI backend and an extendable frontend (mobile/web). Perfect for building intelligent assistants, AI companions, or automation agents.

🚀 Quickstart (Developer)
🔧 Backend — FastAPI

Run the backend locally:

cd backend
python -m venv venv
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app:app --reload --port 8000


The backend provides:

🎤 Speech-to-Text (STT)

🗣️ Text-to-Speech (TTS)

🤖 LLM Gateway

📚 RAG Hooks (Retrieval options)

💻 Frontend (placeholder)

See frontend/README.md for instructions.

Frontend planned features:

Microphone-based voice input

Live transcription

Chat-style UI

Multi-platform support (Web / Mobile / Desktop)

📦 Repository Structure
AI-Agent/
│
├── backend/          # FastAPI backend (STT, TTS, LLM, RAG)
├── frontend/         # React / mobile frontend placeholder
│
├── README.md         # You are here
└── LICENSE           # MIT License

📝 License

This project is licensed under the MIT License, meaning you can use it freely in commercial and open-source projects.
