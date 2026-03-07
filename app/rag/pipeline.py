from .retrieval import retrieve
from .filters import filter
from .llm import build_system_prompt, get_response_from_llm

def rag_pipeline(question):
    results = retrieve(question)
    context, _, doc_found = filter(results["documents"][0], results["distances"][0])
    if not doc_found: return None

    prompt = build_system_prompt(context) #TODO: consider passing question and add it into the prompt
    answer = get_response_from_llm(prompt, question)
    return answer