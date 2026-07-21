from abc import ABC, abstractmethod


class LlmPort(ABC):
    """Abstract port for LLM (Large Language Model) interactions.

    All LLM providers (Ollama, OpenAI, DeepSeek) implement this interface,
    enabling the domain layer to remain decoupled from specific providers.
    """

    @abstractmethod
    def chat(self, system_prompt: str | None, user_prompt: str) -> str:
        """Send a chat request and return the model's response text.

        Args:
            system_prompt: Optional system-level instruction.
            user_prompt: The user message / query.

        Returns:
            The model's text response.
        """
        ...
