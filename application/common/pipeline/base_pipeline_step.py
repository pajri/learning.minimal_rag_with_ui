from __future__ import annotations
from abc import abstractmethod

from application.common.pipeline.pipeline_context import PipelineContext

class BasePipelineStep:
    _next_handler: BasePipelineStep = None

    def set_next(self, handler: BasePipelineStep) -> BasePipelineStep:
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, context: PipelineContext) :
        if self._next_handler:
            self._next_handler.handle(context)
        
        #TODO: handle the case where there is no next handler, maybe raise an exception or return a default value
