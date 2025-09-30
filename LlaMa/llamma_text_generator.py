from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

#Load a small LlaMA model (like TinyLlaMA or LlaMA-2 7B if you have GPU)
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" #Free and tiny variant

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

#Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

#User input
prompt = "Why IT industry is"

#Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

#Generate text
outputs = model.generate(**inputs, max_new_tokens=50, do_sample=True, temperature=0.7)

#Decode output
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)