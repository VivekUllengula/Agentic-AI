from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

#Load a small LlaMA model (like TinyLlaMA or LlaMA-2 7B if you have GPU)
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" #Free and tiny variant

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

#Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def get_bot_response(user_message: str) -> str:
    #Create a chatbot-style prompt
    prompt = (
        "You are a helpful customer support assistant for an e-commerce website.\n"
        f"User: {user_message}\n"
        "Bot:"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        pad_token_id = tokenizer.eos_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("Bot:")[-1].strip()

