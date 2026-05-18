from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.rag.rag_pipeline_context import RagPipelineContext


class PromptBuildingStep(BasePipelineStep):
    def handle(self, rag_context: RagPipelineContext): 
        context = rag_context.documents
        question = rag_context.query

        rag_context.system_prompt = self.build_system_prompt()
        rag_context.user_prompt = self.build_user_prompt(context, question)
        
        self._next_handler.handle(rag_context)

    def build_system_prompt(self):
        return f"""
Answer the question using only the context.

Instructions:
- Use exact words and phrases from the context
- Copy the answer directly from the context whenever possible
- Select the shortest span that fully answers the question
- If multiple contexts are provided, choose the context that contains the most complete answer

Constraints:
- Use only information from the context
- Keep the answer to one sentence

If there is no relevant answer in the contexts, say:
I don't know
"""

    def build_user_prompt(self, contexts, question):
        context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])
        return f"Context:\n{context_lines}\n\nQuestion:\n{question}\n"