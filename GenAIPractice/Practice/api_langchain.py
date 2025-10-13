from langchain.embeddings import HuggingFaceBgeEmbeddings

embeddings = HuggingFaceBgeEmbeddings(model_name="gemini-text-embedding-small")

from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

docs = [
    Document(page_content="FastAPI is a modern Python web framework for APIs."),
    Document(page_content="LangChain helps build applications with LLMs and embeddings."),
    Document(page_content="Gemini embeddings are Google’s embedding model."),
]
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatGoogleGemini

llm = ChatGoogleGemini(model="gemini-2.5-flash-lite")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever()
)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    answer = qa_chain.run(query.question)
    return {"answer": answer}

import gradio as gr

def gradio_query(question):
    return qa_chain.run(question)

gr_interface = gr.Interface(fn=gradio_query, inputs="text", outputs="text")
app = gr.mount_gradio_app(app, gr_interface, path="/gradio")