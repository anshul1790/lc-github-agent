from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load OpenAI key from .env
load_dotenv()

def get_openai_llm():
    # You can add more config/env handling here
    return ChatOpenAI(
        model="gpt-4.1-nano",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2,
    )
