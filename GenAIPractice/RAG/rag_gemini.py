import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#RAG/Langchain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

print("Loading modules...")

# --- Configuration ---
load_dotenv()  # Load environment variables from a .env file if present
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key: 
    raise ValueError("GOOGLE_API_KEY environment variable not set.")    
# Initialize the GenAI client   
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print("Error initializing client. Is GOOGLE_API_KEY set?")
    print(f"Details: {e}")
    exit()

MODEL_NAME = 'gemini-2.5-flash'
MAX_TURNS = 5
DOCUMENT_PATH = "sample.pdf"  # Path to your PDF document

system_instruction = (
    "You are a helpful assistant that uses the provided context to answer user questions. "
    "Your responses must be **grounded** in the provided context from the user's document. "
    "If the context does not contain the answer, you must say 'The required information is not available in my current context. Must... search... further.'"
)

def create_rag_chain(pdf_path: str):
    #Loads doc, creates vector store, and init RAG chain
    try:
        #Data Loading and Chunking
        print("STATUS: Loading document... Must analyze text structure.")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        texts = text_splitter.split_documents(documents)
        print(f"STATUS: Document loaded and split into {len(texts)} chunks.")

        #2 Embedding and Vector Store Creation
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        #Create and in-memory vector store from the document chunks
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
        )

        #Create a retriver for fetching relevant document chunks
        retriever = vectorstore.as_retriever(search_kwargs={"k":3})
        print("STATUS: Vector Store created. Retrieval readiness achieved.")

        #3 Generation Chain

        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=0.6,
            system_instruction=system_instruction,
        )

        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=False
        )
        return rag_chain
    
    except Exception as e:
        print("Error creating RAG chain.")
        print(f"Details: {e}")
        exit()

# --- Main Conversation Loop ---
print(f"Initializing RAG chat with {DOCUMENT_PATH}...")
rag_chain = create_rag_chain(DOCUMENT_PATH)
chat_history = [] # This is for LangChain, NOT the native Gemini ChatSession

for turn in range(1, MAX_TURNS + 1):
    user_input = input(f"[{turn}/{MAX_TURNS}] You: ")

    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("\nChat finished by user. RAG system powered down.")
        break
        
    try:
        # Send the message to the RAG chain
        # The chain performs: User Input -> Retrieval -> Context Augmentation -> Gemini Call
        response = rag_chain.invoke(
            {"question": user_input, "chat_history": chat_history}
        )
        
        # Update chat history for the ConversationalRetrievalChain
        chat_history.append((user_input, response["answer"]))
        
        print(f"Gemini: {response['answer']}\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# --- Cleanup ---
print("--- Final Conversation History ---")
for user_q, model_a in chat_history:
    print(f"User: {user_q}")
    print(f"Model: {model_a}")
    print("-" * 20) 