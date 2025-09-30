from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GOOGLE_MODEL_NAME")

gemini = genai.Client(api_key=api_key)

contents = input("Enter what you want to know about: ")

response = gemini.models.generate_content(
    model=model_name,
    contents=contents,
    config={
        "system_instruction": "You are a helpful assistant, answer as concisely as possible and just give a short answer.",
        "max_output_tokens": 50
    }
)

if __name__ == "__main__":
    print(response.text)