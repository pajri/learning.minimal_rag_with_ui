"""Chain of Responsibility base class for pipeline steps."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.models.pipeline import PipelineContext


class BasePipelineStep(ABC):
    """A single step in a Chain-of-Responsibility pipeline.

    Each concrete step implements :meth:`handle` to process the shared
    *context* and then delegates to :attr:`_next_handler` (if set).

    Usage::

        step_a.set_next(step_b).set_next(step_c)
        step_a.handle(context)
    """

    _next_handler: BasePipelineStep | None = None

    def set_next(self, handler: BasePipelineStep) -> BasePipelineStep:
        """Chain *handler* after this step.  Returns *handler* for fluent chaining."""
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, context: PipelineContext) -> None:
        """Process *context*; call ``self._next_handler.handle(context)`` to continue."""
        if self._next_handler:
            self._next_handler.handle(context)
