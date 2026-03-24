import ollama
import logging
from app.config import LANGUAGE_MODEL
from app.schemas import DocumentResult

logger = logging.getLogger()

def build_system_prompt() -> str:
    return f"""
Answer using ONLY the context below.

Rules:
- Use ONLY the provided context to answer the question.
- If the answer cannot be found in the context, respond exactly with: I don't know
- Ensure the answer fully addresses the question using relevant details from the context
- Be concise, but include all necessary information for correctness
- Do not use outside knowledge
"""

def build_user_prompt(contexts, question):
    context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])

    return f"""
Answer the following question based on given contexts:

Context:
{context_lines}

Question:
{question}
"""

def get_response_from_llm(system_prompt, user_prompt) -> str:
    logger.info(f"using language model: {LANGUAGE_MODEL}")
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]