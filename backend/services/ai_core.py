# backend/services/ai_core.py (Production-ready for Gemini)

import os
import asyncio
import hashlib
from typing import Tuple, Optional
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerationConfig

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in .env")
    client = None
else:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        client = None  # Handle failure gracefully

# --- Design Tool ---

async def handle_design_tool(prompt: str) -> Tuple[str, Optional[str]]:
    """
    Simulates generating a design asset based on the prompt.
    Returns a message and a stable URL for the generated design.
    """
    print(f"[Design Tool] Generating asset for prompt: '{prompt}'")
    await asyncio.sleep(3)  # non-blocking sleep for async context

    # Extract topic from prompt if possible
    design_topic = prompt.split("design a")[1].strip() if "design a" in prompt.lower() else "a creative graphic"

    # Generate a stable URL using MD5 hash of the prompt
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    design_url = f"https://image-api.com/v1/design/{prompt_hash}"

    response_message = (
        f"Design complete! I've created the graphic for '{design_topic}'. "
        f"You can view the full-resolution asset here: {design_url}"
    )

    return response_message, design_url


# --- General LLM / RAG Handler ---

async def handle_llm_query(user_input: str, session_id: str) -> str:
    """
    Handles general AI queries using Gemini LLM.
    If the Gemini client is unavailable, returns an error message.
    """
    if not client:
        return "I'm sorry, the AI service is currently unavailable. Please check the API key."

    # System instruction for AI behavior
    system_instruction = (
        "You are the Canva AI Agent, a helpful, friendly, and concise assistant. "
        "Your primary goal is to help users with design and productivity tasks. "
        "If the user asks for a design, hand the task over to the 'design tool'."
    )

    try:
        # Using Gemini's generate_content method
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Fast chat model
            contents=[user_input],
            config=GenerationConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text

    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return "I'm having trouble connecting to my central processing unit right now. Please try again later."
