from fastapi import FastAPI
from contextlib import asynccontextmanager
import chromadb

from app.rag.embeddings import MyEmbeddingFunctionSentenceTransformer
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = chromadb.PersistentClient(path="./chroma_db")
    embedding_function = MyEmbeddingFunctionSentenceTransformer()
    collection = client.get_or_create_collection(
        name="rag_collection",
        embedding_function=embedding_function
    )

    app.state.collection = collection
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)