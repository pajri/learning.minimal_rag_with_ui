import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# list collections
print("Collections:")
print(client.list_collections())

# get collection
collection = client.get_collection("rag_collection")

# get all data
data = collection.get()

print("\nDocuments:")
for doc in data["documents"]:
    print(doc)

print("\nIDs:")
print(data["ids"])

print("\nEmbeddings length:")
print(len(data["embeddings"]))