from openai import OpenAI
from .message_generator import create_message

client = OpenAI()

def moderate_text(input):
    response = client.moderations.create(
        model = "omni-moderation-latest",
        input = input
    )

    return response

from openai import OpenAI
client = OpenAI()

def get_response_from_llm(system_prompt, user_prompt):
    messages = create_message(system_prompt, user_prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast + good enough
        messages=messages,
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    return result