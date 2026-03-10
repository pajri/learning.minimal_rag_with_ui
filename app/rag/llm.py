import ollama
from app.config import LANGUAGE_MODEL
from app.schemas import DocumentResult


def build_system_prompt(doc_context: list[DocumentResult]) -> str:
    context_lines = "".join([f"- {doc.content}\n" for doc in doc_context])

    return f"""
    You are a helpful chatbot.
    Use only the following pieces of context to answer the question.
    If the answer is not contained, say you don't know.

    Context:
    {context_lines}
    """


def get_response_from_llm(system_prompt: str, input_query: str) -> str:
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_query},
        ],
    )

    return response["message"]["content"]