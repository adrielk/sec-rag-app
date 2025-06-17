# app/pipeline_langchain/chain.py
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class LangChainRAG:
    def __init__(
        self,
        docs_path=None,
        chroma_dir=None,
        chunk_size=500,
        chunk_overlap=100,
        collection_name="mindria-docs",
        model_name="gpt-4o"
    ):
        self.docs_path = docs_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "documents")
        )
        self.chroma_dir = chroma_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "chroma_store")
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        self.model_name = model_name

        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPEN_API_KEY"))
        self.llm = ChatOpenAI(model=self.model_name, openai_api_key=os.getenv("OPEN_API_KEY"))
        self.vectorstore = None
        self.qa_chain = None

    def ingest_documents(self):
        # Load and split documents
        loader = DirectoryLoader(self.docs_path, glob="*.md")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        # Store in Chroma
        self.vectorstore = Chroma.from_documents(
            chunks, self.embeddings, persist_directory=self.chroma_dir, collection_name=self.collection_name
        )
        self.vectorstore.persist()
        print(f"Ingested {len(chunks)} chunks into Chroma at {self.chroma_dir}")

    def setup_qa_chain(self):
        if not self.vectorstore:
            self.vectorstore = Chroma(
                persist_directory=self.chroma_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        retriever = self.vectorstore.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True
        )

    def answer_question(self, question: str):
        if not self.qa_chain:
            self.setup_qa_chain()
        result = self.qa_chain({"query": question})
        return result["result"], result["source_documents"]

if __name__ == "__main__":
    rag = LangChainRAG()
    mode = input("Enter mode (ingest/query): ").strip().lower()
    if mode == "ingest":
        rag.ingest_documents()
    elif mode == "query":
        question = input("Enter your question: ")
        answer, sources = rag.answer_question(question)
        print("\nAnswer:\n", answer)
        print("\nSources:")
        for i, doc in enumerate(sources):
            print(f"\n--- Source {i+1} ---\n{doc.page_content[:500]}...\n")
    else:
        print("Unknown mode. Use 'ingest' or 'query'.")
