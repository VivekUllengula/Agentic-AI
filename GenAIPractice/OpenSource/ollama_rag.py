from ollama import chat
from ollama import ChatResponse

user_prompt = input("Ask you question: ")

messages=[
  {
    'role': 'system',
    'content': 'You are a helpful assistant that answers in a rude manner and in 20 words only.\'',
  },
  {
    'role': 'user',
    'content': f'{user_prompt}',
  }
]
response: ChatResponse = chat(model='gemma3:1b',messages=messages)
print(response.message.content)