"""
Prompt templates module.

Contains base prompt templates used by the LLM client
and interpretation components.
"""


SYSTEM_PROMPT_BASE = """
You are an AI assistant operating under strict system rules.
Always follow the provided system context.
""".strip()


INTERPRETER_PROMPT_TEMPLATE = """
Analyze the user input and return a structured JSON output
according to the specified schema.
""".strip()
