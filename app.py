from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

import chromadb
from chromadb.utils import embedding_functions
from chromadb import Documents, EmbeddingFunction, Embeddings

import ollama

### config ###
DISTANCE_THRESHOLD = 0.7
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

### function definitions ###
# embedding
class MyEmbeddingFunctionSentenceTransformer(EmbeddingFunction):
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.model.encode(
            input, 
            convert_to_numpy=True, normalize_embeddings=True
        )

        embeddings_result = embeddings.tolist()
        return embeddings_result
    
def get_approved_chunks(documents, distances):
    approved_chunks = []
    retrieval_log = []

    for doc, dist in zip(documents, distances):
        retrieval_log.append({'document':doc,'distance':dist})
        if dist <= DISTANCE_THRESHOLD:
            approved_chunks.append(doc)
        
    return approved_chunks, retrieval_log, len(approved_chunks) > 0

def get_response_from_llm(approved_chunks, input_query):
    ### build prompt ###
    context_lines = ''.join([f"- {chunk}\n" for chunk in approved_chunks])

    system_prompt = f"""
    You are a helpful chatbot.
    Use only the following pieces of conetxt to answer the question.
    If the answer is not contained, say you don't know. 

    Context:
    {context_lines}
    """
    print(f'system_prompt: {system_prompt}')

    ### process chat ###
    response = ollama.chat(
        model = LANGUAGE_MODEL, 
        messages = [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : input_query}
        ]
    )

    response_message = response['message']['content']

    return response_message 



### APP and DB setup ###
app = FastAPI()

collection = None

@app.on_event("startup")
def startup():
    global collection

    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=MyEmbeddingFunctionSentenceTransformer()
    )

### request schemas ###
class IngestRequest(BaseModel):
    documents: list[str]

class AskRequest(BaseModel):
    question: str
    k: int = 3

### routes ###
@app.post("/ingest")
def ingest (req: IngestRequest):
    docs = [doc.strip()[:100] for doc in req.documents] # create chunks
    ids = [f"doc_{i}" for i in range(len(docs))]

    collection.add(
        documents=docs,
        ids=ids
    )
    return {"status": "ok", "num_documents": len(docs)}

@app.post("/ask")
def ask(req: AskRequest):
    results = collection.query(
        query_texts=[req.question],
        n_results=req.k
    )

    approved_chunks, retrieval_log, chunks_found = get_approved_chunks(
        results['documents'][0], results['distances'][0])
    
    if not chunks_found:
        print('no sufficiently relevant documents found')

    print('retrieval log:')
    for doc in retrieval_log:
        print(f"Document: {doc['document']}, Distance: {doc['distance']}")

    # return no chunks found message
    response =  "I do not know the answer based the context you provided."
    if chunks_found:
        llm_response = get_response_from_llm(approved_chunks, req.question)
        response = llm_response

    return { "question": req.question, "results": response }