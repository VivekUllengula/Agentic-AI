# worker/fetch_news.py

import os
import requests
import json
import uuid
from datetime import datetime, timezone
from config.settings import BASE_URL, NEWS_API_KEY, DEFAULT_QUERY, MAX_PAGES, PAGE_SIZE, QUEUE_DIR, LOG_DIR
from utils.logger import get_logger

logger = get_logger('fetch_news')

def fetch_articles(query):
    all_articles = []
    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": query,
            "pageSize": PAGE_SIZE,
            "page": page,
            "apiKey": NEWS_API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        logger.info(f"Fetching Page {page} → {response.status_code} → {response.url}")
        response.raise_for_status()
        data = response.json()
        if "articles" in data:
            logger.info(f"Page {page} : Retrieved {len(data['articles'])} articles.")
            all_articles.extend(data["articles"])
        else:
            logger.info(f"Page {page} : No articles found.")
    return all_articles


def save_article(article):
    article_id = str(uuid.uuid4())
    article["fetched_at"] = datetime.now(timezone.utc).isoformat()

    os.makedirs(QUEUE_DIR, exist_ok=True)  # Ensure folder exists
    file_path = os.path.join(QUEUE_DIR, f"{article_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2)
    logger.info(f"Saved article to {file_path}")
    return True


def main():
    logger.info("Starting news fetch task...")
    articles = fetch_articles(query=DEFAULT_QUERY)
    logger.info(f"✅ Total fetched articles: {len(articles)}")

    for idx, article in enumerate(articles):
        if article.get("title") and article.get("url"):
            save_article(article)

if __name__ == "__main__":
    main()
