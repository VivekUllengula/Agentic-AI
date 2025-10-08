
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

tokens = tokenizer(
    ["This is an example sentence", "Each sentence is converted"],
    padding=True,
    truncation=True,
    return_tensors="pt"
)

embeddings = model.encode(tokens['input_ids'], attention_mask=tokens['attention_mask'])
print("Embeddings generated!")  
print(embeddings)

"""
#Generate text using model
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
view = gr.Interface(
    fn=generate,    
    inputs=[gr.Textbox(label="Enter your query")],
    outputs=gr.Textbox(label="Generated Response"),
    title="Gemini-2.5-Flash Text Generation",
    description="Enter a prompt and receive a response from the Gemini-2.5-Flash model.",
    theme="compact",        
    allow_flagging="never",
)
view.launch()
"""