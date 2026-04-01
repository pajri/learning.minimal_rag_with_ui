import re
from ..llm import llm_openai, llm_ollama
from ..llm.prompt_builder import build_faithfulness_prompt

def moderate_output_openai(output):
    response = llm_openai.moderate_text(output)

    if response.results[0].flagged:
        return False, "Unsafe output content detected by OpenAI moderation."
    
    return True, output

def detect_secrets(text):
    # simple API key pattern
    if re.search(r"sk-\w+", text):
        return False, "Sensitive data detected"
    return True, text

def faithfulness_check(output, context):
    prompt = build_faithfulness_prompt(context, output)

    if len(output) > 500:
        # if long, use openai to check faithfulness
        result = llm_openai.get_response_from_llm(None, prompt)
    else:
        result = llm_ollama.get_response_from_llm(None, prompt)

    return "yes" in result.lower()


def filter(output, context):
    # moderate output
    safe, result = moderate_output_openai(output)
    if not safe:
        return False, result
    
    # detect secrets
    safe, result = detect_secrets(output)
    if not safe:
        return False, result
    
    # faithfulness check
    faithful = faithfulness_check(output, context)
    if not faithful:
        return False, "The output contains information that is not supported by the retrieved contexts."

    return True, output