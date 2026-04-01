import re
import logging
from ..llm.llm_openai import moderate_text


logger = logging.getLogger(__name__)

def validate_input(user_input):
    if not user_input or user_input.strip() == "":
        return False, "Input cannot be empty."
    
    if len(user_input) > 1000:
        return False, "Input is too long."
    
    return True, user_input

def sanitize_input(user_input):
    # remove excessive whitespace
    user_input = re.sub(r'\s+', ' ', user_input).strip()

    # remove html/xml tag (simple)
    user_input = re.sub(r'<.*?>', '', user_input)

    return user_input

def moderate_input(user_input):
    BLOCKED_KEYWORDS = ['kill', 'bomb', 'attack']
    for keyword in BLOCKED_KEYWORDS:
        if keyword in user_input.lower():
            return False, "Unsafe content detected."
        
    return True, user_input

def moderate_input_openai(user_input):
    response = moderate_text(user_input)

    if response.results[0].flagged:
        logger.info(f"OpenAI moderation flagged the input: {response}")
        result_categories = response.results[0].categories.model_dump()
        result = f"Unsafe content detected by OpenAI moderation: {', '.join([cat for cat, is_flagged in result_categories.items() if is_flagged])}"
        return False, result
    
    return True, user_input

def detect_injection(user_input):
    INJECTION_PATTERNS = [
        "ignore previous instrucions",
        "act as system",
        "reveal the system prompt",
        "you are now"
    ]

    for pattern in INJECTION_PATTERNS:
        if pattern in user_input.lower():
            return False, "Potential prompt injection detected."
    return True, user_input

def filter(user_input):
    # validate
    logger.info("Validating input...")
    valid, message = validate_input(user_input)
    if not valid:
        return False, message
    
    # sanitize
    logger.info("Sanitizing input...")
    user_input = sanitize_input(user_input)

    # moderate
    logger.info("Moderating input...")
    safe, message = moderate_input(user_input)
    if not safe:
        return False, message
    
    # moderate using openai moderation endpoint
    logger.info("Moderating input with OpenAI...")
    safe, message = moderate_input_openai(user_input)
    if not safe:
        return False, message
    
    # injection detection
    logger.info("Detecting prompt injection...")
    safe, message = detect_injection(user_input)
    if not safe:
        return False, message
    
    return True, user_input
