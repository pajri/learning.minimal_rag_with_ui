import os
from openai import OpenAI
from .message_generator import create_message

def get_response_from_llm_deepseek(system_prompt, user_prompt):
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    messages = create_message(system_prompt, user_prompt)

    response = client.chat.completions.create(
        model="deepseek-chat",  # or deepseek-coder
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content