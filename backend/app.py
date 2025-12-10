from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import asyncio

from .services.ai_core import handle_design_tool, handle_llm_query

# ---------------------------------------------------
# App Initialization
# ---------------------------------------------------
app = FastAPI(title="AI Agent Backend")

# Enable CORS for all origins (you can limit this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Data Models
# ---------------------------------------------------
class ChatRequest(BaseModel):
    user_input: str
    session_id: str

class AgentResponse(BaseModel):
    message: str
    design_result_url: Optional[str] = None


# ---------------------------------------------------
# HELPER — Better Intent Detection
# ---------------------------------------------------
def detect_intent(text: str) -> str:
    text = text.lower()

    design_keywords = ["design", "ui", "ux", "banner", "poster", "logo", "thumbnail"]
    if any(word in text for word in design_keywords):
        return "design"

    return "chat"


# ---------------------------------------------------
# API ROUTES
# ---------------------------------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Agent Backend is operational."}


@app.post("/chat")
async def chat_text(request: ChatRequest) -> AgentResponse:
    logging.info(
        f"[SESSION {request.session_id}] Incoming message: {request.user_input}"
    )

    intent = detect_intent(request.user_input)
    logging.info(f"Detected intent: {intent}")

    response_message = ""
    design_url = None

    # ----------------------------
    # Design Intent
    # ----------------------------
    if intent == "design":
        try:
            response_message, design_url = await handle_design_tool(request.user_input)
        except Exception as e:
            logging.error(f"Design tool error: {e}")
            response_message = (
                "The design tool is currently unavailable. Please try again later."
            )

    # ----------------------------
    # Chat / LLM Intent
    # ----------------------------
    else:
        try:
            response_message = await handle_llm_query(
                request.user_input, request.session_id
            )
        except Exception as e:
            logging.error(f"LLM processing error: {e}")
            response_message = (
                "I'm sorry, I'm having trouble processing your request at the moment."
            )

    # Return the formatted response
    return AgentResponse(
        message=response_message,
        design_result_url=design_url
    )
