"""
Memory store module.

Responsible for persisting and retrieving memory objects.
Contains no business logic.
"""


def store_memory(memory: dict) -> None:
    """
    Persists a new memory object.
    """
    raise NotImplementedError


def update_memory(memory_id: str, updates: dict) -> None:
    """
    Updates fields of an existing memory object.
    """
    raise NotImplementedError


def fetch_memories(
    *,
    types: list[str],
    domains: list[str],
    status: str = "active"
) -> list[dict]:
    """
    Fetches memory objects matching the given filters.
    """
    raise NotImplementedError


def mark_memory_inactive(memory_id: str) -> None:
    """
    Marks a memory object as inactive.
    """
    raise NotImplementedError
