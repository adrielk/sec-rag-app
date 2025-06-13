import os
from typing import List
from embedding import OpenAIEmbedder

class DocumentChunker:
    def __init__(self, folder_path: str, chunk_size: int = 500, overlap: int = 100):
        self.folder_path = folder_path
        self.chunk_size = chunk_size
        self.overlap = overlap

    def read_documents(self) -> List[str]:
        documents = []
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents.append(f.read())
        return documents

    def chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            if end == len(text):
                break
            start += self.chunk_size - self.overlap
        return chunks

    def chunk_all_documents(self) -> List[str]:
        all_chunks = []
        for doc in self.read_documents():
            all_chunks.extend(self.chunk_text(doc))
        return all_chunks

    def generate_embeddings(self) -> list:
        """Generate embeddings for all document chunks using OpenAIEmbedder."""
        embedder = OpenAIEmbedder()
        all_chunks = self.chunk_all_documents()
        embeddings = [embedder.embed_text(chunk) for chunk in all_chunks]
        return embeddings

def main():
    folder = os.path.join(os.path.dirname(__file__), "..", "documents")
    folder = os.path.abspath(folder)
    chunk_size = int(input("Enter chunk size (default 500): ") or 500)
    overlap = int(input("Enter overlap size (default 100): ") or 100)
    chunker = DocumentChunker(folder, chunk_size, overlap)
    all_chunks = chunker.chunk_all_documents()
    print(f"Total chunks created: {len(all_chunks)}")
    for i, chunk in enumerate(all_chunks[:5]):
        print(f"\n--- Chunk {i+1} ---\n{chunk}\n")
    if len(all_chunks) > 5:
        print(f"...and {len(all_chunks) - 5} more chunks.")

    # Test generating embeddings
    print("\nGenerating embeddings for the all chunks...")
    sample_chunks = all_chunks[:20]
    embedder = OpenAIEmbedder()
    for i, chunk in enumerate(sample_chunks):
        embedding = embedder.embed_text(chunk)
        print(f"Embedding for chunk {i+1} (length {len(embedding)}): {embedding[:5]} ...")

if __name__ == "__main__":
    main()
