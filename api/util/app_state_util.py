from fastapi import Request

def get_vectorstore_chunk(request: Request):
    return request.app.state.vectorstore_chunk

def get_vectorstore_question(request: Request):
    return request.app.state.vectorstore_question