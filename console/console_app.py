import json
from app.rag.pipeline import rag_pipeline
from app.ingestion.pipeline import ingestion_pipeline


def main():
    # load data
    with open("./dataset/machine_learning_knowledge.json") as f:
        docs = json.load(f)

    print(docs[0])

if __name__ == "__main__":
    main()