"""
LLM client module.

Provides a single interface for generating LLM responses.
"""


def generate_response(
    system_context: str,
    recent_turns: list[dict],
    user_message: str
) -> str:
    """
    Generates and returns the assistant response.

    Notes:
    - Stateless
    - No memory access
    - No business logic
    """
    raise NotImplementedError
