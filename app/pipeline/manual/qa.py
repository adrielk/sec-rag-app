import os
import openai
from dotenv import load_dotenv

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
