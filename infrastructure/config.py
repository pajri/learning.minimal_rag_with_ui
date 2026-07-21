"""Application-wide settings, loaded from environment / .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root (one level above infrastructure/).
_BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Typed configuration for the RAG application.

    Values can be overridden via environment variables or a ``.env`` file.
    """

    model_config = SettingsConfigDict(
        env_file=str(_BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -- paths -----------------------------------------------------------------
    base_dir: Path = _BASE_DIR
    chroma_persist_dir: str = "./chroma_db"

    # -- model identifiers -----------------------------------------------------
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    language_model: str = "qwen2:0.5b"
    query_expansion_model: str = "deepseek-r1:1.5b"
    evaluation_model: str = "gpt-4o-mini"

    # -- thresholds ------------------------------------------------------------
    distance_threshold: float = 0.5

    # -- API keys --------------------------------------------------------------
    deepseek_api_key: str | None = None
    openai_api_key: str | None = None


# Singleton instance — used by the DI wiring.
settings = Settings()
