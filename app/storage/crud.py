from .initialize import get_collection
def create(document):
    collection = get_collection()
    collection.add(document)
