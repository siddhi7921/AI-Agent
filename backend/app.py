# backend/app.py (Updated)
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# --- NEW: Import the core AI logic ---
from .services.ai_core import handle_design_tool, handle_llm_query 

# ... (Setup and Data Models remain the same) ...

# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Agent Backend is operational."}

@app.post("/chat")
async def chat_text(request: ChatRequest) -> AgentResponse:
    """Handles text input, calls the LLM, and retrieves tools/RAG data."""
    logging.info(f"Received chat request: {request.user_input} (Session: {request.session_id})")

    # 1. NLU/Intent Determination: Use the LLM to decide the best path (Tool or General Chat)
    #    NOTE: The simple keyword check is a temporary stand-in for complex LLM function calling!
    intent = "design" if "design" in request.user_input.lower() else "chat"
    
    response_message = ""
    design_url = None

    if intent == "design":
        # 2. Tool Call: Call the "Canva" design tool function
        try:
            response_message, design_url = await handle_design_tool(request.user_input)
        except Exception as e:
            logging.error(f"Design tool failed: {e}")
            response_message = "I'm sorry, the design tool is currently unavailable."

    else:
        # 3. LLM/RAG: Call the RAG chain or simple LLM
        try:
            response_message = await handle_llm_query(request.user_input, request.session_id)
        except Exception as e:
            logging.error(f"LLM query failed: {e}")
            response_message = "I'm sorry, I couldn't process your request right now."
    
    # 

[Image of AI agent architecture with LLM, Design Tool, and RAG components]

    
    return AgentResponse(
        message=response_message,
        design_result_url=design_url
    )

# ... (speech_to_text endpoint remains the same) ...
