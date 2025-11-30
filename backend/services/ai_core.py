# backend/services/ai_core.py (Updated for Gemini)

import time
import os
from typing import Tuple, Optional
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerationConfig

# Load environment variables from .env file
load_dotenv() 

# Initialize the Gemini Client
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None # Handle failure gracefully

# --- Tool Logic (Remains similar for now) ---

async def handle_design_tool(prompt: str) -> Tuple[str, Optional[str]]:
    """Simulates calling a design service based on the prompt."""
    print(f"Design Tool: Generating asset for prompt: '{prompt}'")
    await time.sleep(3) 

    # In a real app, the LLM would interpret the prompt and then generate the image.
    design_topic = prompt.split("design a")[1].strip() if "design a" in prompt.lower() else "a creative graphic"
    design_url = f"https://image-api.com/v1/design/{hash(prompt)}" 
    
    response_message = (
        f"Design complete! I've created the graphic for '{design_topic}'. "
        f"You can view the full-resolution asset now."
    )
    return response_message, design_url


# --- General LLM/RAG Implementation (Now uses an actual LLM) ---

async def handle_llm_query(user_input: str, session_id: str) -> str:
    """Handles general chat using the Gemini LLM."""
    if not client:
        return "I'm sorry, the AI service is currently unavailable. Please check the API key."
    
    # 1. RAG Lookup (Placeholder): If you had RAG, you'd insert context here
    # context = rag_lookup(user_input, session_id) 
    # full_prompt = f"Use the following context: {context}\n\nUser Question: {user_input}"
    
    system_instruction = (
        "You are the Canva AI Agent, a helpful, friendly, and brief assistant. "
        "Your primary goal is to help users with design and productivity tasks. "
        "If the user asks for a design, be ready to hand the task over to the 'design tool'."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # A fast model suitable for chat
            contents=[user_input],
            config=GenerationConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
        
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return "I seem to be having trouble connecting to my central processing unit right now."
