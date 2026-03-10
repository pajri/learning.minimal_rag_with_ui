from fastapi import FastAPI
from contextlib import asynccontextmanager
import chromadb
import logging

from app.rag.embeddings import MyEmbeddingFunctionSentenceTransformer
from routes import router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting app")

    logger.info("initializing db")
    client = chromadb.PersistentClient(path="./chroma_db")
    embedding_function = MyEmbeddingFunctionSentenceTransformer()
    collection = client.get_or_create_collection(
        name="rag_collection",
        embedding_function=embedding_function
    )
    logger.info("done initializing db")

    app.state.collection = collection
    yield

    logger.info("shutting down app")

app = FastAPI(lifespan=lifespan)
app.include_router(router)