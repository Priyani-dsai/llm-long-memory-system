"""
Memory injection module.

Translates resolved memory rules into system-level
instructions consumable by the LLM.
"""

from typing import List, Dict


def _format_constraint(memory: Dict) -> str:
    return f"You must {memory.get('domain')}."


def _format_commitment(memory: Dict) -> str:
    return f"You have committed to {memory.get('domain')}."


def _format_instruction(memory: Dict) -> str:
    return f"You should {memory.get('domain')}."


def _format_preference(memory: Dict) -> str:
    return f"If possible, you should {memory.get('domain')}."


FORMATTERS = {
    "constraint": _format_constraint,
    "commitment": _format_commitment,
    "instruction": _format_instruction,
    "preference": _format_preference,
}


TYPE_ORDER = [
    "constraint",
    "commitment",
    "instruction",
    "preference",
]


def build_system_context(
    resolved_memories: List[Dict]
) -> str:
    """
    Builds system-level instruction text for the LLM
    from resolved memory rules.
    """
    if not resolved_memories:
        return ""

    lines: List[str] = []

    for memory_type in TYPE_ORDER:
        for memory in resolved_memories:
            if memory.get("type") == memory_type:
                formatter = FORMATTERS.get(memory_type)
                if formatter:
                    lines.append(formatter(memory))

    return "\n".join(lines)
