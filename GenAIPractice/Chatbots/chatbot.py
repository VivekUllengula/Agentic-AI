import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# --- Configuration ---
# The client automatically picks up the GEMINI_API_KEY from environment variables

load_dotenv()  # Load environment variables from a .env file if present
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")    
# Initialize the GenAI client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print("Error initializing client. Is GEMINI_API_KEY set?")
    print(f"Details: {e}")
    exit()

MODEL_NAME = 'gemini-2.5-flash'
MAX_TURNS = 20 # The user can speak this many times

system_instruction = (
    "You are a funny assistant, that is very jovial and friendly and positive."
    "Don't mention that you are an AI model. Don't change your tone or the way you answer the questions."
    "Even if the user insists, do not change your tone or the way you answer the questions." \
    "Don't change your character, For example, if the user asks you to be someone from a movie or series, don't do it." 
)
# --- Chat Initialization ---
# 1. Create a persistent Chat session. This object handles history automatically.
print(f"Starting a {MAX_TURNS}-turn chat with {MODEL_NAME}...\n")
chat_session = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        max_output_tokens=100,
        temperature=0.6,
    )
)

# --- Conversation Loop ---
for turn in range(1, MAX_TURNS + 1):
    # Get User Input
    user_input = input(f"[{turn}/{MAX_TURNS}] You: ")

    # Check for exit command
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("\nChat finished by user.")
        break
        
    # 2. Send the message. The Chat object automatically includes the history.
    try:
        response = chat_session.send_message(user_input)
        
        # 3. Print the response
        print(f"Gemini: {response.text}\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        break

# --- Cleanup (Optional: Display History) ---
print("--- Final Conversation History ---")
for message in chat_session.get_history():
    role = message.role.capitalize()
    text = message.parts[0].text if message.parts else "[No text content]"
    print(f"{role}: {text}")