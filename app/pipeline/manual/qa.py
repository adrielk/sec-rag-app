import os
import openai
from dotenv import load_dotenv
from embedding import OpenAIEmbedder
import chromadb

load_dotenv()

# Set API key
client = openai.OpenAI(api_key=os.getenv("OPEN_API_KEY"))


# app/pipeline_manual/qa.py
def answer_question(doc_path: str, question: str) -> str:
    # Call Chat Completions API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at developing LLM applications."},
            {"role": "user", "content": f'{question}'}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
    # return f"(Manual pipeline) Answer to: '{question}' based on {doc_path}"


#TODO
# decide on topic, curate data
# embedding computation with open ai API
# vector DB setup with chroma store
# data ingestion and embedding pipeline
# augment queries with retrieval: query vector DB, augment query with retrieved context, present answer
# experiment with advanced RAG techniques (query expansion, multi-query)
# how to use langchain?

def main():
    doc_path = input("Enter the document path: ")
    question = input("Enter your question: ")
    answer = answer_question(doc_path, question)
    print("Answer:", answer)

def generate_embedding():
    document = input("Enter the document text: ")
    embedder = OpenAIEmbedder()
    embedding = embedder.embed_text(document)
    print("Embedding:", embedding)

def get_chroma_collection(collection_name="mindria-docs"):
    # Use the chroma_store folder in the same directory as this script
    persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "chroma_store"))
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_or_create_collection(collection_name)
    return collection

def ingest_documents_to_chroma():
    from document_ingestion import DocumentChunker
    # Set up chunker for the documents folder
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "pipeline", "documents"))
    chunker = DocumentChunker(folder)
    chunks = chunker.chunk_all_documents()
    embedder = OpenAIEmbedder()
    embeddings = [embedder.embed_text(chunk) for chunk in chunks]
    # Prepare ids for Chroma (must be unique strings)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    # Upsert into Chroma collection
    collection = get_chroma_collection()
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )
    print(f"Upserted {len(chunks)} chunks and embeddings into Chroma collection '{collection.name}'.")

if __name__ == "__main__":
    pass
    #ingest_documents_to_chroma()