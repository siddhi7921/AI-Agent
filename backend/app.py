# backend/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# --- Setup ---
app = FastAPI(title="AI-Agent Core Backend")
logging.basicConfig(level=logging.INFO)

# Define CORS settings to allow your frontend to communicate
origins = [
    "http://localhost:5173", # Your Vite development server
    "https://your-agent-frontend.vercel.app", # Your deployed Vercel domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models (for Request/Response) ---
class ChatRequest(BaseModel):
    """Model for text-based chat input."""
    user_input: str
    session_id: str # For context management/memory

class AgentResponse(BaseModel):
    """Model for the agent's response, matching your frontend AgentTypes.ts."""
    message: str
    design_result_url: str | None = None # Use None for optional fields


# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Agent Backend is operational."}

@app.post("/chat")
async def chat_text(request: ChatRequest) -> AgentResponse:
    """Handles text input, calls the LLM, and retrieves tools/RAG data."""
    logging.info(f"Received chat request: {request.user_input} (Session: {request.session_id})")

    # 1. NLU: Determine the user's intent (Chat, Design, Reminder, Search)
    intent = "design" if "design" in request.user_input.lower() else "chat"
    
    response_message = "I am processing your request..."
    design_url = None

    if intent == "design":
        # 2. Tool Call: Call the "Canva" design tool function
        # response_message, design_url = await handle_design_tool(request.user_input)
        response_message = f"I've initiated the design for '{request.user_input}'. "
        design_url = "https://placeholder-design.com/123" 
    else:
        # 3. LLM/RAG: Call the RAG chain or simple LLM
        # response_message = await handle_llm_query(request.user_input, request.session_id)
        response_message = f"Understood. The LLM would now respond to: {request.user_input}"
    
    return AgentResponse(
        message=response_message,
        design_result_url=design_url
    )

@app.post("/stt")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """Handles audio file upload and converts it to text (STT)."""
    # 1. Save file: Save audio_file.file to a temporary location
    # 2. Process: Call a model (e.g., Whisper) to transcribe the audio
    # 3. Return Text: return {"text": "Transcribed text here"}
    return {"text": "This is a placeholder for your transcribed voice input."}
