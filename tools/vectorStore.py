import chromadb
from chromadb.utils import embedding_functions
from data.cities import CITY_FACTS


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.Client()
collection = client.get_or_create_collection("cities", embedding_function=ef)


def populate_vector_store():
    if collection.count() > 0:
        return
    for city, facts in CITY_FACTS.items():
        collection.add(
            documents=[facts],
            ids=[city],
            metadatas=[{"city": city}]
        )


def query_vector_store(city: str):
    results = collection.query(query_texts=[city], n_results=2)
    # print(results)  # debug
    if not results["documents"]:
        return False, ""
    if results["distances"][0][0] < 0.8:
        return True, results["documents"][0][0]
    return False, ""