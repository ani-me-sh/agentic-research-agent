from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(model="gemma4:e4b", temperature=0)
llama_llm = ChatOllama(model="llama3.1:latest", temperature=0)
