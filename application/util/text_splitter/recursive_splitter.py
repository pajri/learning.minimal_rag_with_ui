from langchain_text_splitters import RecursiveCharacterTextSplitter

def recursive_text_split(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "]
    )

    # split documents
    chunked_docs = splitter.split_documents(documents)

    return chunked_docs