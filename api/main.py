import chromadb
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from langchain_huggingface import HuggingFaceEmbeddings

from application.storage.setup import setup_question_storage
from application.config import EMBEDDING_MODEL
from application.storage.setup import setup_chunk_storage, setup_question_storage

from api.routes import router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting app")

    logger.info("initializing db")
    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True}
    )
    
    vectorstore_chunk = setup_chunk_storage(embedding_function)
    vectorstore_question = setup_question_storage(embedding_function)

    logger.info("done initializing db")

    app.state.vectorstore_chunk = vectorstore_chunk
    app.state.vectorstore_question = vectorstore_question
    yield

    logger.info("shutting down app")

app = FastAPI(lifespan=lifespan)
app.include_router(router)