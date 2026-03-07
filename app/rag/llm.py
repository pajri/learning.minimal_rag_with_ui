import ollama
from app.config import LANGUAGE_MODEL


def build_system_prompt(approved_chunks: list[str]) -> str:
    context_lines = "".join([f"- {chunk}\n" for chunk in approved_chunks])

    return f"""
You are a helpful chatbot.
Use only the following pieces of context to answer the question.
If the answer is not contained, say you don't know.

Context:
{context_lines}
"""


def get_response_from_llm(approved_chunks: list[str], input_query: str) -> str:
    system_prompt = build_system_prompt(approved_chunks)

    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_query},
        ],
    )

    return response["message"]["content"]