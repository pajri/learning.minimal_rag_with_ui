Hexagonal Architecture Refactoring — Complete ✅

  New directory structure:
```
  code_ui/
  ├── domain/                          # NEW — Pure business logic
  │   ├── ports/                       # 5 ABCs (LlmPort, VectorStorePort, ...)
  │   ├── models/                      # PipelineContext, RagPipelineContext
  │   ├── services/                    # prompt_service, chunking_service, retrieval_service
  │   └── pipeline/                    # Chain of Responsibility + 6 steps
  │
  ├── infrastructure/                  # NEW — Driven adapters
  │   ├── config.py                    # Settings (pydantic-settings, loaded from .env)
  │   ├── llm/                         # OllamaProvider, OpenAIProvider, DeepSeekProvider
  │   ├── vector_store/chroma_store.py # ChromaDB adapter
  │   ├── embedding/                   # HuggingFace embedding adapter
  │   ├── filtering/                   # 7 ContentFilterPort implementations + Composite
  │   └── reranker/                    # CrossEncoder adapter
  │
  ├── application/                     # REFACTORED — Use-case orchestrators
  │   ├── dto/                         # Data transfer objects
  │   ├── services/                    # IngestionService, RagService, FilteringService
  │   └── pipeline_factory.py          # Assembles the Chain-of-Responsibility pipeline
  │
  ├── api/                             # REFACTORED — Thin controllers
  │   ├── dependencies.py              # NEW — All DI wiring
  │   ├── routes.py                    # ≈50% smaller, delegates to services
  │   └── main.py                      # Minimal lifespan, no infra setup
  │
  └── console/console_app.py           # FIXED — imports + interactive loop
```

  Key improvements:

| Before                                         | After                                      |
| ---------------------------------------------- | ------------------------------------------ |
| `import ollama` hardcoded in pipeline steps    | `LlmPort` injected via constructor         |
| `routes.py` had JSON parsing + filtering logic | Thin handlers, delegates to `*Service`     |
| Three LLM files with no common interface       | All implement `LlmPort` ABC                |
| Vector stores on `app.state` (FastAPI-only)    | `ChromaStore` implements `VectorStorePort` |
| Duplicated filter/prompt code                  | Single implementation in domain services   |
| Flat config module                             | `Settings` class with `pydantic-settings`  |
| 4-step filter function                         | Composite pattern — 5 independent filters  |
| `console/console_app.py` broken imports        | Fully wired + interactive loop             |


  Architecture constraint verified:
```
  $ grep -r "import (fastapi|ollama|chromadb|openai|langchain_community)" domain/
```
# No matches found ✓

  The old files under application/rag/, application/llm/, application/ingestion/, application/storage/, application/filtering/, and application/common/ still exist on disk but are no longer imported by the API layer. You can delete them when ready.
