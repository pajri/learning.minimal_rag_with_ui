import ollama
import logging

from application.config import LANGUAGE_MODEL
from .message_generator import create_message

logger = logging.getLogger()

def get_response_from_llm(system_prompt, user_prompt):
    logger.info(f"using language model: {LANGUAGE_MODEL}")
    messages = create_message(system_prompt, user_prompt)

    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=messages,
    )

    return response["message"]["content"]