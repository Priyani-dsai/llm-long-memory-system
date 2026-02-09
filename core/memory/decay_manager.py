"""
Memory decay manager.

Handles confidence decay and inactivation of memories.
"""

from core.memory.memory_store import fetch_memories, update_memory


DECAY_RATE = 0.05
MIN_CONFIDENCE = 0.2


def apply_decay(current_turn: int) -> None:
    """
    Applies confidence decay to inactive memories.
    """

    memories = fetch_memories(
        types=[],
        domains=[],
        status="active",
    )

    for memory in memories:
        turns_unused = current_turn - memory.get("last_used_turn", current_turn)

        if turns_unused <= 0:
            continue

        new_confidence = memory["confidence"] - (DECAY_RATE * turns_unused)

        if new_confidence < MIN_CONFIDENCE:
            update_memory(
                memory_id=memory["memory_id"],
                updates={
                    "status": "inactive",
                    "confidence": new_confidence,
                },
            )
        else:
            update_memory(
                memory_id=memory["memory_id"],
                updates={
                    "confidence": new_confidence,
                },
            )
