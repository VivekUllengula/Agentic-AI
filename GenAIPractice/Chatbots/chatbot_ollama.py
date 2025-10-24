from gradio import themes
import gradio as gr
from ollama import chat

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.vectorstores import Chroma  # Make sure correct import

OLLAMA_MODEL = "gemma3:1b"

# -------------------
# Load PDF & create vector store
# -------------------
print("Loading the document...")
loader = PyPDFLoader("BajiBabu_Resume.pdf")
documents = loader.load()

print("Splitting into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)
print(f"Document split into {len(texts)} chunks.")

print("Creating embeddings and vector store...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = Chroma.from_documents(documents=texts, embedding=embeddings)
print("Vector store ready!")

# -------------------
# Chatbot Class with RAG
# -------------------
class ChatBot:
    def __init__(self, system_prompt, vector_store=None):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.vector_store = vector_store
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def ask(self, user_input):
        # Retrieve relevant context if vector_store is available
        context_text = ""
        if self.vector_store:
            docs = self.vector_store.similarity_search(user_input, k=3)  # top 3 relevant chunks
            context_text = "\n".join([doc.page_content for doc in docs])
            if context_text:
                self.add_message("system", f"Use the following document context to answer:\n{context_text} and if you don't have enough information just say so.")

        # Add user message
        self.add_message("user", user_input)

        # Call Ollama
        response = chat(model=OLLAMA_MODEL, messages=self.messages)
        reply = response.get("message", {}).get("content", "")
        self.add_message("assistant", reply)
        return reply

# Initialize bot with vector store
bot = ChatBot(
    "You are a helpful assistant, that gives clear and concise answers.",
    vector_store=vector_store
)

# -------------------
# Gradio Chat function
# -------------------
def gradio_chat(user_input, history):
    reply = bot.ask(user_input)
    history.append((user_input, reply))
    return "", history

# -------------------
# Launch Gradio
# -------------------
with gr.Blocks(theme=themes.Glass()) as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type your message")
    msg.submit(gradio_chat, [msg, chatbot], [msg, chatbot])

demo.launch()
