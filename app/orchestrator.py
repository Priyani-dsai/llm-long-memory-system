"""
Orchestrator module.

This module controls the end-to-end execution of a single
conversation turn by coordinating all core components.
"""


def process_turn(
    user_message: str,
    turn_id: int
) -> str:
    """
    Runs the full pipeline for a single user turn
    and returns the assistant response.

    Contractual flow (DO NOT change order):
    1. interpreter.interpret_turn
    2. retriever.retrieve_memories
    3. conflict_resolver.resolve_conflicts
    4. injector.build_system_context
    5. llm_client.generate_response
    6. update short-term context
    """
    raise NotImplementedError
