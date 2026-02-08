"""
Memory injection module.

Translates resolved memory rules into system-level
instructions for the LLM.
"""


def build_system_context(
    resolved_memories: list[dict]
) -> str:
    """
    Builds system-level instruction text for the LLM.

    Rules:
    - Declarative statements only
    - Ordered by rule strength
    - No internal schema leakage
    """
    raise NotImplementedError
