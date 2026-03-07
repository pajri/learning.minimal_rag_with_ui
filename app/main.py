from fastapi import FastAPI
from contextlib import asynccontextmanager
import chromadb

from app.rag.embeddings import MyEmbeddingFunctionSentenceTransformer
from app.routes import router, set_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")
    yield
    print("App shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(router)