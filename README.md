# RAG with API (FastAPI + ChromaDB + Ollama)

This project implements a **simple Retrieval-Augmented Generation (RAG) system exposed through a REST API**.

The goal of this project is to learn and practice the core building blocks of RAG:
- document ingestion
- embedding and vector storage
- similarity-based retrieval
- relevance filtering
- LLM response generation

The implementation is intentionally minimal so each step of the pipeline is explicit and easy to follow.

---

## Overview

**High-level flow:**

1. Documents are ingested through an API endpoint  
2. Text is embedded using a sentence-transformer model  
3. Embeddings are stored in a vector database (ChromaDB)  
4. When a question is asked:
   - relevant chunks are retrieved using vector similarity
   - results are filtered using a distance threshold
   - the remaining context is passed to an LLM
5. The API returns an answer grounded only in retrieved context

---

## Tech Stack

- **API Framework**: FastAPI  
- **Vector Database**: ChromaDB  
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)  
- **LLM Runtime**: Ollama  
- **Language Model**: Llama-3.2-1B-Instruct (GGUF)  
- **Language**: Python  

---

## Project Structure

```
.
|-- app.py                  # app file
|-- cat-facts.txt           # the dataset
|-- request_ask.json        # sample request for /ask
|-- requests_ingest.json    # sample request for /ingest
`-- README.md
```

---

## Setup

### 1. Install dependencies

```
pip install fastapi uvicorn chromadb sentence-transformers ollama
```

### 2. Start Ollama

```
ollama serve
```

Pull the model if it is not already available:

```
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

---

## Running the API

```
uvicorn app:app --reload
```

Once running, the API will be available at:

- Base URL: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

---

## API Endpoints

### 1. Ingest Documents

**POST** `/ingest`

**Sample request** (`requests_ingest.json`):

```
{
  "documents": [
    "A cat can run at a top speed of approximately 31 mph.",
    "A cat’s heart beats nearly twice as fast as a human heart."
  ]
}
```

**Response:**

```
{
  "status": "ok",
  "num_documents": 2
}
```

**Notes:**
- Documents are lightly chunked before embedding
- Each chunk is embedded and stored in ChromaDB

---

### 2. Ask a Question

**POST** `/ask`

**Sample request** (`request_ask.json`):

```
{
  "question": "How fast can a cat run?",
  "k": 3
}
```

**Sample response:**

```
{
  "question": "How fast can a cat run?",
  "results": "A cat can travel at a top speed of approximately 31 mph."
}
```

If no retrieved documents pass the relevance filter:

```
{
  "results": "I do not know the answer based the context you provided."
}
```

---

## Relevance Filtering

After retrieval, results are filtered using a **distance threshold**:

- Only documents with `distance <= DISTANCE_THRESHOLD` are used
- This ensures the model only answers using sufficiently relevant context
- If no documents pass the threshold, the system explicitly returns an unknown response

This helps keep responses grounded and avoids unsupported answers.

---

## Design Notes

- The RAG pipeline is implemented without external frameworks
- Each stage (embedding, retrieval, filtering, generation) is handled explicitly
- The API boundary makes the system easy to test, debug, and extend

---

## Possible Extensions

- Persistent vector storage
- Improved chunking strategy
- Retrieval quality evaluation (e.g. precision@k)
- Streaming LLM responses
- Framework-based retrievers or chains (such as langchain)
- Authentication and rate limiting

---

## License

For learning and experimentation purposes.
