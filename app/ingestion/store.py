from app.storage.initialize import get_collection

def store_documents(docs, ids):
    collection = get_collection()
    collection.add(documents=docs, ids=ids)