"""
LLM client module
"""

import requests
import time
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "5m",
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
            "num_predict": 300
        }
    }

    for attempt in range(2):
        try:
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=120
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

    # Detect schedule-style query
    lower_msg = user_message.lower()
    is_schedule_query = (
        "tomorrow" in lower_msg
        or "schedule" in lower_msg
        or "what do i have" in lower_msg
        or "what do i have tomorrow" in lower_msg
    )

    # HARD GUARD:
    # If user is asking about future schedule
    # but system_context is empty → do NOT hallucinate.
    if is_schedule_query and not system_context.strip():
        return (
            "I do not have any stored commitments or tasks "
            "for that date in memory."
        )

    # Build short conversation context
    context_lines = []
    for turn in recent_turns[-2:]:
        context_lines.append(f"User: {turn['user']}")
        context_lines.append(f"Assistant: {turn['assistant']}")

    context_block = "\n".join(context_lines)

    # Strong grounding instruction
    grounding_instruction = (
        "You must answer ONLY using the system rules provided. "
        "If the system rules do not contain relevant information, "
        "say that no relevant memory exists. "
        "Do NOT invent calendar events, meetings, or tasks."
    )

    prompt = (
        f"You are an assistant.\n\n"
        f"{grounding_instruction}\n\n"
        f"System rules:\n{system_context}\n\n"
        f"Conversation so far:\n{context_block}\n\n"
        f"User: {user_message}\n"
        f"Assistant:"
    )

    return call_llm(prompt)

