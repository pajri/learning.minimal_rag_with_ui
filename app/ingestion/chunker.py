from ..util.text_splitter.nltk_splitter import nltk_text_split
from ..util.text_splitter.recursive_splitter import recursive_text_split

def chunk_id_generator(chunked_docs):
    chunk_counter = {}
    for doc in chunked_docs:
        doc_id = doc.metadata["id"]

        if doc_id not in chunk_counter:
            chunk_counter[doc_id] = 0

        chunk_index = chunk_counter[doc_id]
        doc.metadata["chunk_id"] = f"{doc_id}_chunk{chunk_index}"
        chunk_counter[doc_id] += 1

    return chunked_docs

def chunk_docs(documents):
    # chunked_docs = nltk_text_split(documents)
    chunked_docs = recursive_text_split(documents)
    chunked_docs = chunk_id_generator(chunked_docs)
    
    return chunked_docs