"""
LLM client module
"""

import requests
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


import time

def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
        }
    }

    for attempt in range(2):
        try:
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.exceptions.ReadTimeout:
            if attempt == 0:
                time.sleep(2)
            else:
                raise



def generate_response(
    system_context: str,
    recent_turns: List[Dict],
    user_message: str
) -> str:
    """
    Generates the assistant's natural language response.
    """

    context_lines = []
    for turn in recent_turns:
        context_lines.append(f"User: {turn['user']}")
        context_lines.append(f"Assistant: {turn['assistant']}")

    context_block = "\n".join(context_lines)

    prompt = (
        f"You are an assistant.\n\n"
        f"System rules:\n{system_context}\n\n"
        f"Conversation so far:\n{context_block}\n\n"
        f"User: {user_message}\n"
        f"Assistant:"
    )

    return call_llm(prompt)
