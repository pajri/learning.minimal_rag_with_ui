import os 
from langchain_community.vectorstores import Chroma

def setup_storage(embedding_function, collection_name):
    dir = '../chroma_db/{collection_name}'
    os.makedirs(dir, exist_ok=True)
    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory=dir,
        collection_name=collection_name
    )

    return vectorstore

def setup_chunk_storage(embedding_function):
    return setup_storage(embedding_function, "rag_collection")

def setup_question_storage(embedding_function):
    return setup_storage(embedding_function, "rag_question")
