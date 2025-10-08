import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai.types import Content, Part
from typing import List, Tuple

# Load env vars
load_dotenv()

# --- Global Initialization ---
# Use GEMINI_API_KEY as the standard for the new GenAI SDK
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") 
model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash")

if not api_key:
    # It's good practice to alert the user if the key is missing
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set.")

# Init client
client = genai.Client(api_key=api_key) 


# --- Helper Function for History Conversion ---
def transform_gradio_history(history: List[Tuple[str, str]]) -> List[Content]:
    """
    Converts Gradio's history (list of user/assistant string pairs)
    into the GenAI SDK's list of Content objects for the chat history.
    """
    contents: List[Content] = []
    
    # Gradio history is a list of [user_msg, bot_msg] pairs.
    for user_msg, bot_msg in history:
        # User message
        contents.append(
            Content(role="user", parts=[Part.from_text(text=user_msg)])
        )
        # Assistant message
        contents.append(
            Content(role="model", parts=[Part.from_text(text=bot_msg)])
        )
        
    return contents


# --- Gradio Chat Function (Fixed) ---
def gemini_chat(message: str, history: List[Tuple[str, str]]):
    """
    Sends the user message to the Gemini model using the correct streaming method 
    and maintaining history by re-initializing the chat session.
    """
    
    # 1. Transform Gradio history into the GenAI Content format
    gemini_history = transform_gradio_history(history)
    
    # 2. Re-initialize the chat session with the full history
    # This solves the multi-user/clear history issues.
    chat_session = client.chats.create(model=model_name, history=gemini_history)
    
    # 3. Use the correct streaming method: stream_send_message() (FIXED)
    # The 'send_message' method in the new SDK does not take 'stream=True'.
    response_stream = chat_session.send_message_stream(message)

    # 4. Yield the streamed response text
    full_response = ""
    for chunk in response_stream:
        # GenAI streaming chunks might have text or other data
        if chunk.text:
            full_response += chunk.text
            yield full_response

# --- Create the Gradio Chat Interface (Fixed) ---
demo = gr.ChatInterface(
    fn=gemini_chat,
    title="Gemini Chatbot with Gradio",
    description=f"Ask the Gemini model ({model_name}) anything! Uses the `google-genai` SDK and streaming.",
    # Removed deprecated/renamed arguments for Gradio v4.0+ (FIXED)
    # retry_btn="Try Again",
    # clear_btn="Clear History"
    
    # Use the recommended message type (FIXED)
    type='messages' 
)

# Launch the application
if __name__ == "__main__":
    demo.launch()