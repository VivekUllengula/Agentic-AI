from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()
client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

class TextInput(BaseModel):
    text: str
    language: str = "hi"

@router.post("/prompt_chain")
async def prompt_chain (input: TextInput):

    #Step 1: Summarize Text
    summary = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Summarize the text"},
            {"role": "user", "content": input.text}
        ],
        temperature= 0.4
    ).choices[0].message.content
    
    #Step 2: Check for Grammar

    grammar = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Check for grammar"},
            {"role": "user", "content": input.text}
        ],
        temperature= 0.4
    ).choices[0].message.content

    #Step 3: Translate

    translate = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": f"Translate the text to {input.language}"},
            {"role": "user", "content": grammar}
        ],
        temperature= 0.4
    ).choices[0].message.content

    return {
        "summary": summary,
        "grammar": grammar,
        "translate": translate
    }