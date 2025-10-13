from google import genai
import os
from dotenv import load_dotenv
import gradio as gr

# Load env vars
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash")

# Init client
gemini = genai.Client(api_key=api_key)

def generate(contents):
    response = gemini.models.generate_content(
        model=model_name,
        contents=contents,
        config={
            "max_output_tokens": 50,
            "system_instruction": "You are a helpful assistant that is always serious, and uses harsh",
        }
    )
    return response.text

# Launch Gradio UI
gr.Interface(
    fn=generate,
    inputs=[gr.Textbox(label="Enter your query")],
    outputs=gr.Textbox(
        label="AI Response",
        lines=6,         # starting height
        max_lines=30,    # grows until 30 lines, then scrolls
        interactive=False   # output only (user can’t edit)
    ),
    title="Gemini-2.5-Flash Text Generation",
).launch( share=True)
