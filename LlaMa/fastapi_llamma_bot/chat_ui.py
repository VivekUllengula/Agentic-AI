import streamlit as st
import requests

st.set_page_config(page_title="TinyLLaMA Chatbot")

st.title("Tiny LLaMA Customer Support Bot")

#For storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#User input
user_input = st.text_input("You:", key="input")

#Send message to FastAPI
def get_bot_reply(message):
    url = "http://localhost:8000/chat"
    response = requests.post(url, json={"message": message})
    return response.json()["reply"]

#When user submits message
if user_input:
    st.session_state.messages.append(("You", user_input))
    reply = get_bot_reply(user_input)
    st.session_state.messages.append(("Bot", reply))
    st.rerun()

#Display chat history
for sender, msg in st.session_state.messages:
    st.markdown(f"**{sender}:** {msg}")