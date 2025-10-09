import os
import json
import asyncio
import aiohttp
import aiofiles # Import aiofiles for async file operations
from pathlib import Path
from fastapi import FastAPI, Query
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Load environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_ENDPOINT = os.getenv("NEWS_API_ENDPOINT", "https://newsapi.org/v2/everything")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash-latest")

# Configuring fastapi
app = FastAPI()

genai.configure(api_key=GOOGLE_API_KEY)

#Making sure the path exists
OUTPUT_DIR = Path("news_output")
OUTPUT_DIR.mkdir(exist_ok=True)

#Instatiating genai model
model = genai.GenerativeModel(MODEL_NAME)

#Fetching news from news api
async def fetch_news(query: str, page_size: int =5):
    """ Fetching news from API"""
    url = f"{NEWS_API_ENDPOINT}?q={query}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data.get("articles", [])
        
async def rewrite_news_with_gemini(news_item: dict):
    """Call Gemini LLM to rewrite title & content"""
    original_title = news_item.get('title','')
    original_content = news_item.get('content', news_item.get('description', ''))

    #Avoid sending empty request to the API
    if not original_title and not original_content:
        return "No content to rewrite"
    
    prompt = f"""
    Rewrite the following news title and content for clarity and engagement.
    Provide the rewritten title first, followed by "---", and then the rewritten content.
    Example:
    Rewritten Title Here
    ---
    Rewritten content starts here...

    Original Title: {original_title}
    Original Content: {original_content}
    """

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    
    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return "Error in rewriting"
    
def sanitize_filename(name:str) -> str:
    if not name:
        return f"news_{int(Path().stat().st_mtime)}"
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

@app.get("/news")
async def get_news(query: str = Query(..., description="Search query for news") ):
    articles = await fetch_news(query)

    if not articles:
        return {"status": "error", "message": "No articles found or failed to fetch news."}
    
    rewrite_tasks = [rewrite_news_with_gemini(article) for article in articles]
    rewritten_contents = await asyncio.gather(*rewrite_tasks)

    results = []
    for idx, article in enumerate(articles):
        title_safe = sanitize_filename(article.get("title", f"news_{idx}"))
        filename = OUTPUT_DIR / f"{title_safe}.json"

        news_data = {
            "original_title": article.get("title"),
            "original_content": article.get("content", article.get("description")),
            "rewritten_content": rewritten_contents[idx],
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt"),
            "source": article.get("source", {}).get("name")
        }

        async with aiofiles.open(filename, "w", encoding="utf-8") as f:
            await f.write(json.dumps(news_data, ensure_ascii=False, indent=4))

        results.append(news_data)

    return {"status": "success", "count": len(results), "data": results}
