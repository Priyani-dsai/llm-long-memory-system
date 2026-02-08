"""
Memory extractor module.

Responsible for extracting atomic, structured memory
objects from user input based on interpreter output.
"""


def extract_memories(
    user_message: str,
    interpreter_output: dict,
    turn_id: int
) -> list[dict]:
    """
    Extracts zero or more atomic memory objects from the user message.

    Returns:
        A list of memory objects matching the schemas defined
        in memory_schema.py.

    Notes:
    - This function MUST NOT store memory.
    - It only returns structured memory candidates.
    - Memory policy signals must be respected.
    """
    raise NotImplementedError
