import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
import gensim.downloader as api
import uuid

# Initialize Qdrant client
qdrant = QdrantClient("http://localhost:6333")

# Load Word2Vec model
word2vec_model = api.load("word2vec-google-news-300")

# Collection name
collection_name = "sensitive_terms"

# Load Bag of Words from JSON
def load_bag_of_words(file_path="bag_of_words.json"):
    with open(file_path, 'r') as file:
        return json.load(file)

# Create Qdrant collection for storing vector embeddings
def initialize_qdrant():
    if qdrant.collection_exists(collection_name):
        qdrant.delete_collection(collection_name=collection_name)
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=300, distance="Cosine"),
    )
    print(f"Collection '{collection_name}' initialized in Qdrant.")


# Add sensitive terms to Qdrant
def add_terms_to_qdrant(bag_of_words):
    points = []
    for term, category in bag_of_words.items():
        if term in word2vec_model:
            vector = word2vec_model[term]
            # Generate a UUID for each term
            term_id = str(uuid.uuid4())  # Generate a valid UUID for the term
            points.append(
                PointStruct(
                    id=term_id,  # Use the UUID as the ID
                    vector=vector.tolist(),
                    payload={"category": category, "term": term},  # Store term in the payload
                )
            )
    qdrant.upsert(collection_name=collection_name, points=points)
    print("Sensitive terms added to Qdrant.")

# Query Qdrant for similar terms
def query_similar_terms(query_term, top_k=5):
    if query_term in word2vec_model:
        query_vector = word2vec_model[query_term]
        results = qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector.tolist(),
            limit=top_k,
        )
        # Include original term from payload
        return [
            {
                "term": result.payload.get("term", "Unknown Term"),  # Retrieve original term from payload
                "category": result.payload.get("category", "Unknown Category"),
                "score": result.score,
            }
            for result in results
        ]
    else:
        print(f"'{query_term}' not found in Word2Vec model.")
        return []


# Example usage
if __name__ == "__main__":
    # Load Bag of Words dynamically from JSON
    bag_of_words = load_bag_of_words()

    initialize_qdrant()
    add_terms_to_qdrant(bag_of_words)

    # Query similar terms dynamically
    while True:
        query_term = input("Enter a term to query for similar terms (or type 'exit' to quit): ").strip()
        if query_term.lower() == 'exit':
            print("Exiting the program.")
            break

        similar_terms = query_similar_terms(query_term)
        if similar_terms:
            print(f"Similar terms for '{query_term}':")
            for term_info in similar_terms:
                print(f"Term: {term_info['term']}, Category: {term_info['category']}, Score: {term_info['score']:.2f}")
        else:
            print(f"No similar terms found for '{query_term}'.")
