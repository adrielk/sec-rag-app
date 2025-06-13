import os
import openai
from dotenv import load_dotenv

load_dotenv()

class OpenAIEmbedder:
    def __init__(self, api_key=None, model="text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPEN_API_KEY")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)

    def embed_text(self, text: str):
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
