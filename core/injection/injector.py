"""
Memory injection module.
"""

from typing import List, Dict


def _format_constraint(memory: Dict) -> str:
    return f"You must strictly follow this constraint: {memory.get('domain')}."


def _format_commitment(memory: Dict) -> str:
    scope = memory.get("scope", {})
    domain = memory.get("domain")

    if scope.get("type") == "date" and scope.get("value"):
        return f"Commitment: You have committed to {domain} on {scope.get('value')}."
    
    return f"Commitment: You have committed to {domain}."


def _format_instruction(memory: Dict) -> str:
    return f"Instruction: You should follow guidance related to {memory.get('domain')}."


def _format_preference(memory: Dict) -> str:
    domain = memory.get("domain")
    scope = memory.get("scope", {})

    if scope.get("type") == "global":
        return f"User preference: In general, prefer {domain} in accordance with previously stated constraints."

    if scope.get("type") == "date":
        return f"User preference: For {scope.get('value')}, prefer {domain}."

    return f"User preference related to {domain}."



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


def build_system_context(resolved_memories: List[Dict]) -> str:
    if not resolved_memories:
        return ""

    lines: List[str] = [
        "You must strictly obey the following memory constraints and preferences:"
    ]

    for memory_type in TYPE_ORDER:
        for memory in resolved_memories:
            if memory.get("type") == memory_type:
                formatter = FORMATTERS.get(memory_type)
                if formatter:
                    lines.append("- " + formatter(memory))

    return "\n".join(lines)

