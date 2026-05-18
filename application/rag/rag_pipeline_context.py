from application.common.pipeline.pipeline_context import PipelineContext

class RagPipelineErrorResponse:
    pipeline_name: str = ""
    error_message: str = ""

class RagPipelineContext(PipelineContext):
    documents: list = []
    approved_chunks: list = []
    query: str = ""
    model: str = "deepseek-r1:1.5b"
    expanded_queries: list = []
    user_prompt: str = ""
    system_prompt: str = ""
    answer: str = ""
    vectorstore_chunk = None 
    vectorstore_question = None
    
    status: str = ""
    error_response: RagPipelineErrorResponse = None


