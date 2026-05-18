import logging

from langchain_core.documents import Document

from application.rag.context_retrieval_step import ContextRetrievalStep
from application.rag.query_expansion_step import QueryExpansionStep
from application.rag.reranking_step import RerankingStep
from application.rag.prompt_building_step import PromptBuildingStep
from application.rag.llm_pipeline_step import LlmPipelineStep
from application.rag.rag_pipeline_context import RagPipelineContext

logger = logging.getLogger(__name__)

def rag_pipeline(vectorstore_chunk, vectorstore_question, question):
    rag_context = RagPipelineContext()
    rag_context.vectorstore_chunk = vectorstore_chunk
    rag_context.vectorstore_question = vectorstore_question
    rag_context.query = question

    query_expansion_step = QueryExpansionStep()
    context_retrieval_sep = ContextRetrievalStep()
    reranking_step = RerankingStep()
    prompt_building_step = PromptBuildingStep()
    llm_pipeline_step = LlmPipelineStep()

    query_expansion_step \
        .set_next(context_retrieval_sep) \
        .set_next(reranking_step) \
        .set_next(prompt_building_step) \
        .set_next(llm_pipeline_step)
    
    query_expansion_step.handle(rag_context)
    
    if rag_context.error_response is not None:
        pipeline_name = rag_context.error_response.pipeline_name
        error_message = rag_context.error_response.error_message
        print(f"an error occured in pipeline {pipeline_name}. errpr: {error_message}")

        # TODO return error message
        return rag_context.answer, \
            rag_context.documents, \
            rag_context.system_prompt, \
            rag_context.user_prompt 

    return rag_context.answer, \
            rag_context.documents, \
            rag_context.system_prompt, \
            rag_context.user_prompt 

    """
    logger.info("start rag pipeline")

    print(f"question: {question}")
    expanded_question = expand_query(question)
    print(f"expanded_question: {expanded_question}")

    # context_result_question, _ = get_context_based_on_question_mapping(vectorstore_chunk, vectorstore_question, question)
    context_result_question = []

    context_result = []
    for q in expanded_question:
        _context_result = get_context_based_on_question(vectorstore_chunk, q)
        context_result.extend(_context_result)    

    logger.info(f"context_result_question: {context_result_question}")
    logger.info(f"context_result: {len(context_result)}")
    print(f"context_result: {len(context_result)}")

    contexts = [
        *(context_result_question or []),
        *(context_result or [])
    ]
        
    contexts = ensure_unique_context(contexts)
    print(f"unique context len: {len(contexts)}")

    # HERE
    system_prompt = build_system_prompt()

    if len(contexts) == 0: return None, None, system_prompt, None #doc not found

    contexts = clean_filtered_context(contexts)
    
    print(f"before rerank: ")
    print(contexts)
    contexts = rerank(question, contexts)
    print(f"after rerank: ")
    print(contexts)
    
    user_prompt = build_user_prompt(contexts, question)

    answer = get_response_from_llm(system_prompt, user_prompt)
    # answer = get_response_from_llm_deepseek(system_prompt, user_prompt)
    logger.info("end rag pipeline")

    return answer, contexts, system_prompt, user_prompt
    """