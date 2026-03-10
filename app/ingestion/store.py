def store_documents(collection, documents):
    docs = [doc.content for doc in documents]
    ids = [doc.id for doc in documents]
    collection.add(documents=docs, ids=ids)