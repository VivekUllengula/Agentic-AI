import os
from dotenv import load_dotenv
import gradio as gr

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

#Loading the enivronment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GOOGLE_MODEL_NAME")

#Creating an inference LLM
llm = ChatGoogleGenerativeAI(model=MODEL)

pdf_path = "sample2.pdf"

#Creating the RAG chain
def create_rag_chain(path: str):
    print("Loading the PDF...")
    loader = PyPDFLoader(path)
    documents = loader.load()

    #Splitting the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    #Using the text spitter to split the documents
    texts = text_splitter.split_documents(documents)
    print(f"Document loaded and split into {len(texts)} chunks.")

    #Creating the embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    #Storing the generated embeddings ia a Chroma vector database
    vector_store = Chroma.from_documents(
        documents=texts,
        embedding=embeddings
    )

    #Creating a retriever from the vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    print("Vector store has been created. Retrieval readiness achieved.")

    #Defining the prompt template for context and question
    template = """
    You are a helpful assistant. Use the following documents chunks as reference to answer the question.
    If you don't find an answer in the context, say "I couldn't find that information in the document.

    Context:{context}

    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    #Building a RAG chain with the retriever and the prompt template
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff", #merges context into prompt
        chain_type_kwargs={"prompt": prompt}
    )

    return rag_chain

#Intialize the RAG system
chain = create_rag_chain(pdf_path)

#Ask a question
def ask_question(question, history) -> str:
    response = chain.run(question)
    return response

#Creating the gradio interface

gr.ChatInterface(
    fn=ask_question,
    title="Document Q&A with RAG",
    description="Ask questions about the content of the uploaded PDF document.",
    theme="compact"
).launch(share=True)




