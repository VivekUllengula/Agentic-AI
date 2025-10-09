"""from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

sentence = "Example sentence to tokenize"

tokens = tokenizer.encode(sentence)
texts = tokenizer.tokenize(sentence)
embeddings = model.encode(sentence)

print(f"Tokens Encoded: {tokens}\n")
print(f"Text Tokens: {texts}\n")
print(f"Embeddings: {embeddings}")
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GOOGLE_MODEL_NAME")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

outputs = embeddings.embed_query("This is an example for embeddings")

print(outputs)

