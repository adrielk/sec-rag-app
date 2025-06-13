import os
from embedding import OpenAIEmbedder
import chromadb

class ChromaDocumentQuery:
    def __init__(self, collection_name="mindria-docs"):
        persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "chroma_store"))
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = OpenAIEmbedder()

    def query(self, question: str, n_results: int = 5):
        query_embedding = self.embedder.embed_text(question)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances"]
        )
        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        return list(zip(docs, distances))

if __name__ == "__main__":
    question = input("Enter your question: ")
    n_results = int(input("How many results? (default 5): ") or 5)
    query_engine = ChromaDocumentQuery()
    results = query_engine.query(question, n_results)
    for i, (doc, dist) in enumerate(results):
        print(f"\n--- Result {i+1} (distance: {dist:.4f}) ---\n{doc}\n")
