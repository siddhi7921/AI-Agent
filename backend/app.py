from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio

from .services.ai_core import handle_design_tool, handle_llm_query

# -------------------------------
# App & Middleware
# -------------------------------
app = FastAPI(title="AI Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Data Models
# -------------------------------
class ChatRequest(BaseModel):
    user_input: str
    session_id: str

class AgentResponse(BaseModel):
    message: str
    design_result_url: Optional[str] = None

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Agent Backend is operational."}

@app.post("/chat")
async def chat_text(request: ChatRequest) -> AgentResponse:
    logging.info(f"Received chat request: {request.user_input} (Session: {request.session_id})")

    # Simple intent detection
    intent = "design" if "design" in request.user_input.lower() else "chat"

    response_message = ""
    design_url = None

    if intent == "design":
        try:
            response_message, design_url = await handle_design_tool(request.user_input)
        except Exception as e:
            logging.error(f"Design tool failed: {e}")
            response_message = "I'm sorry, the design tool is currently unavailable."
    else:
        try:
            response_message = await handle_llm_query(request.user_input, request.session_id)
        except Exception as e:
            logging.error(f"LLM query failed: {e}")
            response_message = "I'm sorry, I couldn't process your request right now."

    return AgentResponse(
        message=response_message,
        design_result_url=design_url
    )
