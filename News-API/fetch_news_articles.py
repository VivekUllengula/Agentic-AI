import os, uuid, json, requests
from uuid import uuid4
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv() #Loading the dotenv to get the api from ebv variables

app = FastAPI() #Initiating the Fast API

NEWS_API_URL = "https://newsapi.org/v2/everything?q="
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ARTICLES_DIR = "articles" 
os.makedirs(ARTICLES_DIR, exist_ok=True) #Creating the articles directory

def save_articles_as_json(article):
    uid = str(uuid.uuid4())
    filepath = os.path.join(ARTICLES_DIR, f"{uid}.json")
    with open(filepath, "w") as f:
        json.dump(article, f, indent=2)

@app.get("/fetch-news")
def fetch_news(query: str = "technology", count: int = 5):
    url = f"{NEWS_API_URL}{query}&pageSize={count}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": response.text}
    
    articles = response.json().get("articles", [])

    for article in articles:
        save_articles_as_json(article)

    return{
        "message":f"{len(articles)} articles are fetched"
    }

