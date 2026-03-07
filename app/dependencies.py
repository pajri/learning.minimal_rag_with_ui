from fastapi import Request

def get_collection(request: Request):
    return request.app.state.collection