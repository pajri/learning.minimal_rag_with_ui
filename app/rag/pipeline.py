import logging

from .retrieval import retrieve
from .filters import filter
from .llm import build_system_prompt, get_response_from_llm
from app.schemas import DocumentResult

logger = logging.getLogger()

def rag_pipeline(collection, question):
    logger.info("start rag pipeline")
    results = retrieve(collection, question)
    doc_result = []
    for id, content, dist in zip(results['ids'][0], results['documents'][0], results['distances'][0]):
        _doc = DocumentResult(id=id, content=content, distance=dist)
        doc_result.append(_doc)

    doc_context, _, doc_found = filter(doc_result)
    if not doc_found: return None, None

    prompt = build_system_prompt(doc_context) #TODO: consider passing question and add it into the prompt
    answer = get_response_from_llm(prompt, question)
    logger.info("end rag pipeline")

    return answer, doc_context



