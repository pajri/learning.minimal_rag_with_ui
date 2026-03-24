from langchain_text_splitters import RecursiveCharacterTextSplitter

def recursive_text_split(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "]
    )

    # split documents
    chunked_docs = splitter.split_documents(documents)

    return chunked_docs