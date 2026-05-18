import ollama
import logging 
import json
import re

from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.rag.rag_pipeline_context import RagPipelineContext

class QueryExpansionStep(BasePipelineStep):
    
    def handle(self, context: RagPipelineContext) :
        logger = logging.getLogger()
        model = context.model
        query = context.query
        prompt = f"""
Generate 3 alternative search queries.

Rules:
- Return ONLY a list like this: ["q1", "q2", "q3"]
- No explanation
- No numbering
- No extra text

Query: "{query}"
"""
        response = ollama.chat(
            model = model, 
            messages = [{"role":"user", "content":prompt}]
            )
        
        response_content = response['message']['content']
        logger.info(f"repsonse_content; {response_content}, type: {type(response_content)}")

        expanded_queries = self.extract_queries(response_content)
        logger.info(f"expanded_queries; {expanded_queries}, type: {type(expanded_queries)}")
        
        expanded_queries.append(query)
        context.expanded_queries = expanded_queries

        self._next_handler.handle(context)
    
    def extract_queries(self, text):
        try:
            # Try clean JSON first
            return json.loads(text)
        except:
            pass

        # Extract JSON-like list
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

        # Fallback: split lines
        lines = text.split("\n")
        queries = []
        for line in lines:
            line = line.strip("-•1234567890. ").strip()
            if len(line) > 5:
                queries.append(line)

        return queries