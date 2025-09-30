from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

# Load model (FP16 works best on GPU, CPU will fallback to float32)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-0.6B",
    device_map="auto",
)

# Use CPU
device = "cpu"
model = model.to(device)
print("Model loaded!")

# Prompt text
text = "The weather today "

# Tokenize
inputs = tokenizer(text, return_tensors="pt").to(device)

# Generate text
outputs = model.generate(
    **inputs,
    temperature=0.2,
    max_new_tokens=100,
    do_sample=True,
    eos_token_id=tokenizer.eos_token_id
)

# Decode output
generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Generated Text:\n", generated)
