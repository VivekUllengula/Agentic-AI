import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GOOGLE_MODEL_NAME")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model=MODEL)

file_path = "sample2.pdf"


def create_rag_chain(path: str):
    print("Loading the PDF...")
    loader = PyPDFLoader(path)
    documents = loader.load()

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)
    print(f"Document loaded and split into {len(texts)} chunks.")

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Store in Chroma vector database
    vector_store = Chroma.from_documents(
        documents=texts,
        embedding=embeddings
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    print("Vector Store created. Retrieval readiness achieved.")

    # Define prompt template for context + question
    template = """
    You are a helpful assistant. Use the following document excerpts to answer the question.
    If you don't find an answer in the context, say "I couldn't find that information in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # Build Retrieval-Augmented Generation chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  # merges context into prompt
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain


# Initialize the RAG system
qa_chain = create_rag_chain(file_path)

# Ask a question
question = input("Ask your question:")
result = qa_chain.invoke({"query": question})

print("\nAnswer:")
print(result["result"])
