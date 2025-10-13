from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.embeddings import HuggingFaceBgeEmbeddings

# -----------------------------
# Load SentenceTransformer
# -----------------------------
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Create an embedding function compatible with Chroma
embeddings = HuggingFaceBgeEmbeddings(model_name=model_name)

# -----------------------------
# Create Chroma vector store
# -----------------------------
vector_store = Chroma(embedding_function=embeddings)

# -----------------------------
# Add documents
# -----------------------------
sentences = [
    "Artificial intelligence is transforming the world.",
    "Machine learning is a subset of AI.",
    "Python is a popular programming language.",
    "FastAPI is great for building APIs quickly."
]

# Wrap each sentence in a Document object
docs = [Document(page_content=sent) for sent in sentences]

# Add documents to Chroma
vector_store.add_documents(docs)

print("✅ Documents added to vector store!")

# -----------------------------
# Perform similarity search
# -----------------------------
query = "Tell me about AI and machine learning"

# Retrieve top 2 most similar documents
results = vector_store.similarity_search(query, k=2)

print("\n Top Matches:")
for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}: {doc.page_content}")
