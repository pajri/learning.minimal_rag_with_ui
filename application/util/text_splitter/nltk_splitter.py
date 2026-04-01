import nltk
from nltk.tokenize import sent_tokenize

from langchain_core.documents import Document

def nltk_text_split(documents):
    nltk.download('punkt_tab')
    n_sentences = 2

    chunked_docs = []
    for doc in documents:
        text = doc.page_content
        sentences = sent_tokenize(text)
        
        for i in range(0, len(sentences), n_sentences):
            chunk = " ".join(sentences[i:n_sentences])
            chunked_docs.append(Document(metadata=doc.metadata, page_content=chunk))
    
    return chunked_docs