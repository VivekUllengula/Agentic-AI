import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
import gradio as gr
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

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

app = FastAPI()

pdf_path = "BajiBabu_Resume.pdf"

# =========================
# Database (Postgres via SQLAlchemy)
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback for local/dev if Postgres env is not set; replace with your Postgres URL
    # Example Postgres URL: postgresql+psycopg2://user:password@localhost:5432/mydb
    DATABASE_URL = "postgresql+psycopg2://postgres:Vivek%40007@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(32), nullable=False)  # 'user' | 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("ChatSession", back_populates="messages")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# Pydantic Schemas
# =========================

class SessionCreate(BaseModel):
    title: Optional[str] = None


class SessionOut(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AskRequest(BaseModel):
    question: str


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# RAG Chain creation
# =========================
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
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    # Note: With langchain_chroma, specifying persist_directory handles persistence automatically

    results = vector_store.similarity_search("What is AI?", k=3)

    for doc in results:
        print(doc.page_content)

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

# Global Gradio session id holder (created when running as __main__)
GRADIO_SESSION_ID: Optional[int] = None

#Ask a question
def ask_question(question, history) -> str:
    # Run the RAG chain to generate the assistant answer
    assistant_answer = chain.run(question)

    # If we have an active Gradio session id, persist user and assistant messages
    if GRADIO_SESSION_ID is not None:
        db = SessionLocal()
        try:
            user_message = ChatMessage(session_id=GRADIO_SESSION_ID, role="user", content=question)
            db.add(user_message)
            db.commit()
            db.refresh(user_message)

            assistant_message = ChatMessage(session_id=GRADIO_SESSION_ID, role="assistant", content=assistant_answer)
            db.add(assistant_message)
            db.commit()
            db.refresh(assistant_message)
        finally:
            db.close()

    return assistant_answer



# =========================
# FastAPI Endpoints
# =========================

@app.on_event("startup")
def on_startup() -> None:
    # Ensure tables exist at startup
    Base.metadata.create_all(bind=engine)


@app.post("/sessions", response_model=SessionOut)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    new_session = ChatSession(title=payload.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


@app.get("/sessions", response_model=List[SessionOut])
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    return sessions


@app.get("/sessions/{session_id}/messages", response_model=List[MessageOut])
def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    session_obj = db.get(ChatSession, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return messages


@app.post("/sessions/{session_id}/ask")
def ask_in_session(session_id: int, payload: AskRequest, db: Session = Depends(get_db)):
    session_obj = db.get(ChatSession, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    # Store user question
    user_message = ChatMessage(session_id=session_id, role="user", content=payload.question)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Generate assistant response via RAG chain
    assistant_answer = chain.run(payload.question)

    # Store assistant answer
    assistant_message = ChatMessage(session_id=session_id, role="assistant", content=assistant_answer)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {
        "answer": assistant_answer,
        "user_message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
    }


#Creating the gradio interface (guarded for script run only)
glass_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)

if __name__ == "__main__":
    # Ensure tables exist when running Gradio-only
    Base.metadata.create_all(bind=engine)

    # Create a chat session for this Gradio run
    _db = SessionLocal()
    try:
        session_title = f"Gradio Session - {datetime.utcnow().isoformat()}"
        _session = ChatSession(title=session_title)
        _db.add(_session)
        _db.commit()
        _db.refresh(_session)
        GRADIO_SESSION_ID = _session.id
    finally:
        _db.close()

    gr.ChatInterface(
        fn=ask_question,
        title="Document Q&A with RAG",
        description="Ask questions about the content of the uploaded PDF document.",
        theme=glass_theme
    ).launch(share=True)






