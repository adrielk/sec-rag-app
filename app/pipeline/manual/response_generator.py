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

        #TODO incorporate query expansion:

        return response.choices[0].message.content

    def generate_response_with_expansion(self, question: str) -> str:
        # 1. Generate query expansion (hypothetical answer)
        expansion_prompt = (
            f"Given the following question, generate a hypothetical answer using your general knowledge. "
            f"Do not say you don't know. Be concise.\n"
            f"Question: {question}\n"
            f"Hypothetical Answer:"
        )
        expansion_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": expansion_prompt}
            ],
            temperature=0.7
        )
        hypothetical_answer = expansion_response.choices[0].message.content.strip()
        print(f'Hypothetical Answer: {hypothetical_answer}')

        # 2. Use the expanded query (question + hypothetical answer) to retrieve relevant chunks
        expanded_query = f"{question}\n{hypothetical_answer}"
        # Use the expanded query to retrieve relevant chunks
        results = self.query_engine.query(expanded_query, self.n_results)
        context_chunks = [doc for doc, _ in results]
        context = "\n---\n".join(context_chunks)

        # Reuse the prompt logic from generate_response, but with the new context
        prompt = (
            f"Use the following context to answer the user's question as accurately as possible based on the context below\n"
            f"If the question cannot be answered based on the given context, simply say you don't know. Be strict with how you answer questions and do not hallucinate answers.\n"
            f"Keep your answers reasonably brief.\n"
            f"Context:\n{context}\n"
            f"Question: {question}\n"
        )
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
        answer = generator.generate_response_with_expansion(question)
        print("\nAugmented Answer:\n", answer)
