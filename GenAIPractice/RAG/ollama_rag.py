from ollama import chat, embeddings
from ollama import ChatResponse

from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """
Technology is rapidly evolving, impacting nearly every aspect of our daily lives. 
From artificial intelligence and automation to the widespread adoption of smart devices,
innovations are continually reshaping how we work, communicate, and solve problems.
Cloud computing and data analytics have become integral in business operations,
while cybersecurity is more important than ever as digital threats increase.
The pace of change ensures that staying updated with the latest tech trends is both a challenge and an opportunity.
"""

print("Splitting the text into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
chunks = splitter.split_text(text)
print(f"Split into {len(chunks)} chunks")

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="all-MiniLM-L6-v2")

vector_store = Chroma.from_documents(chunks, embeddings)






