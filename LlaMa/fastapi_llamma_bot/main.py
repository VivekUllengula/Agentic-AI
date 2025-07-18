from fastapi import FastAPI
from pydantic import BaseModel
from bot import get_bot_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def root():
    return {"message": "Welcome to the TinyLLaMA Chatbot API!"}

@app.post("/chat", response_model=ChatResponse)
def chat(chat_request: ChatRequest):
    user_message = chat_request.message
    reply = get_bot_response(user_message)
    return ChatResponse(reply=reply)