"""
Memory decay manager.

Handles aging, reinforcement, and inactivation of memories.
"""


def apply_decay(
    current_turn: int
) -> None:
    """
    Updates confidence and status of memories based on usage
    and time elapsed.
    """
    raise NotImplementedError
