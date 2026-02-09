"""
LLM client module (mock implementation).

Provides a deterministic stand-in for a real LLM,
used for testing and end-to-end pipeline validation.
"""

from typing import List, Dict


def generate_response(
    system_context: str,
    recent_turns: List[Dict],
    user_message: str
) -> str:
    """
    Generates a mock assistant response.

    This implementation is intentionally simple and deterministic.
    It allows us to verify that:
    - system rules are injected correctly
    - short-term context is passed correctly
    - the pipeline works end-to-end
    """

    response_lines = []

    if system_context:
        response_lines.append("[SYSTEM RULES APPLIED]")
        response_lines.append(system_context)

    if recent_turns:
        response_lines.append("\n[RECENT CONTEXT]")
        for turn in recent_turns:
            response_lines.append(f"User: {turn['user']}")
            response_lines.append(f"Assistant: {turn['assistant']}")

    response_lines.append("\n[USER INPUT]")
    response_lines.append(user_message)

    response_lines.append("\n[ASSISTANT RESPONSE]")
    response_lines.append(
        "Acknowledged. I will respond while respecting the above rules."
    )

    return "\n".join(response_lines)
