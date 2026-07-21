"""Pure functions for building LLM prompts.

These functions have zero dependencies on frameworks or infrastructure —
they only manipulate strings.
"""

from langchain_core.documents import Document


def build_system_prompt() -> str:
    """Build the system prompt that constrains the LLM to use only context."""
    return """Answer the question using only the context.

Instructions:
- Use exact words and phrases from the context
- Copy the answer directly from the context whenever possible
- Select the shortest span that fully answers the question
- If multiple contexts are provided, choose the context that contains the most complete answer

Constraints:
- Use only information from the context
- Keep the answer to one sentence

If there is no relevant answer in the contexts, say:
I don't know"""


def build_user_prompt(contexts: list[Document], question: str) -> str:
    """Build a user prompt that presents contexts and the question."""
    context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])
    return f"Context:\n{context_lines}\n\nQuestion:\n{question}\n"


def build_faithfulness_prompt(contexts: list[Document], output: str) -> str:
    """Build a prompt used to evaluate answer faithfulness against contexts."""
    context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])
    return f"""You are a strict evaluator.

Determine whether the answer is fully supported by the given context.

Rules:
- Answer YES if the answer is fully supported
- Answer NO if there is any unsupported or incorrect information

Context:
{context_lines}

Answer:
{output}"""
