from transformers import GPT2Tokenizer, GPT2Model
import torch

#  1. Load pre-trained GPT-2 tokenizer
# This tokenizer knows how to split text into tokens the same way GPT-2 was trained.
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

#  2. Load pre-trained GPT-2 model (only the base transformer, no language head)
# This model returns embeddings and contextualized outputs.
model = GPT2Model.from_pretrained("gpt2")

#  3. Input text
text = "I want to study Python"

#  4. Tokenize the text and return as PyTorch tensors
# return_tensors="pt" tells tokenizer to return PyTorch tensors (pt = PyTorch)
inputs = tokenizer(text, return_tensors="pt")

#  5. Get embeddings from model
# torch.no_grad() disables gradient calculations (saves memory, we aren't training)
with torch.no_grad():
    outputs = model(**inputs)

#  6. Get the output of the final transformer layer
# outputs.last_hidden_state has shape: [batch_size, num_tokens, hidden_size]
# Each token has a 768-dimensional vector (for GPT2 base)
embeddings = outputs.last_hidden_state  # shape: [1, 5, 768] for this sentence

#  7. Get actual tokens for display
tokens = tokenizer.tokenize(text)

#  8. Print token and its corresponding 768-d vector
for i, token in enumerate(tokens):
    print(f" Token: {token}")
    print(f"Embedding (768 values):\n{embeddings[0][i]}")
    print("--------------------------------------------------")
