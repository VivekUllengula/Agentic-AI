import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GOOGLE_MODEL_NAME")

#Langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model=MODEL)

message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "You are an assistant that is angry, reply in that way.",
        },
        {"type": "text", "text": "Hello"},
    ]
)

result = llm.invoke([message])
print(result.content)


    






