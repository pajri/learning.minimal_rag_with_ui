import logging
import json

from langchain_core.documents import Document

from .filters import filter
from .llm import build_system_prompt, build_user_prompt, get_response_from_llm

logger = logging.getLogger()

def clean_filtered_context(contexts):
    for c in contexts:
        if c.page_content.startswith(". "):
            c.page_content = c.page_content.lstrip(". ")

    return contexts

def get_context_based_on_question_mapping(vectorstore_chunk, vectorstore_question, question):
    q_results = vectorstore_question.similarity_search_with_score(question, k=1)
    q_results = [q for q in q_results if q[1] < 0.4]

    doc_ids = []
    for doc, _ in q_results:
        doclist = json.loads(doc.metadata["docs"])
        doc_ids.extend(doclist)
    doc_ids = list(dict.fromkeys(doc_ids))

    if (len(doc_ids) == 0): return None, None
    
    doc_query_result = vectorstore_chunk._collection.get(
        where={"id": {"$in": doc_ids}}
    )

    if(doc_query_result is None): return None, None

    doc_result = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(doc_query_result["documents"], doc_query_result["metadatas"])
    ]

    return doc_result, q_results

def get_context_based_on_question(vectorstore_chunk, question):
    contexts = vectorstore_chunk.similarity_search_with_score(question, k=3)
    contexts = filter(contexts)

    return contexts


def ensure_unique_context(contexts):
    seen = set()
    unique_contexts = []

    for doc in contexts:
        content = doc.page_content.strip()
        
        if content not in seen:
            seen.add(content)
            unique_contexts.append(doc)

    contexts = unique_contexts
    return contexts

def rag_pipeline(vectorstore_chunk, vectorstore_question, question):
    logger.info("start rag pipeline")

    context_result_question, _ = get_context_based_on_question_mapping(vectorstore_chunk, vectorstore_question, question)
    # context_result_question = []
    context_result = get_context_based_on_question(vectorstore_chunk, question)

    logger.info(f"context_result_question: {context_result_question}")
    logger.info(f"context_result: {len(context_result)}")

    contexts = [
        *(context_result_question or []),
        *(context_result or [])
    ]
    
    contexts = ensure_unique_context(contexts)
    if len(contexts) == 0: return None, None #doc not found

    contexts = clean_filtered_context(contexts)

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(contexts, question)

    answer = get_response_from_llm(system_prompt, user_prompt)
    logger.info("end rag pipeline")

    return answer, contexts, system_prompt, user_prompt
