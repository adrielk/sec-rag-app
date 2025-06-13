import os
from embedding import OpenAIEmbedder
from query_documents import ChromaDocumentQuery
import openai
from dotenv import load_dotenv

load_dotenv()

class AugmentedResponseGenerator:
    def __init__(self, collection_name="mindria-docs", n_results=5, model="gpt-4o"):
        self.query_engine = ChromaDocumentQuery(collection_name)
        self.n_results = n_results
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    def generate_response(self, question: str) -> str:
        # Retrieve relevant chunks from ChromaDB
        results = self.query_engine.query(question, self.n_results)
        context_chunks = [doc for doc, _ in results]
        context = "\n---\n".join(context_chunks)
        # Compose augmented prompt
        prompt = (
            f"Use the following context to answer the user's question as accurately as possible based on the context below\n"
            f"If the question cannot be answered based on the given context, simply say you don't know. Be strict with how you answer questions and do not hallucinate answers.\n"
            f"Keep your answers reasonably brief.\n"
            f"Context:\n{context}\n"
            f"Question: {question}\n"
        )
        # Query GPT model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    generator = AugmentedResponseGenerator()

    while True: 
        question = input("Enter your question: ")
        answer = generator.generate_response(question)
        print("\nAugmented Answer:\n", answer)
