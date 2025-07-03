import os,uuid, requests, json
from datetime import datetime, timezone
from utils.logger import get_logger
from utils.image_handler import handle_aricle_image
from tqdm import tqdm
from config.settings import (
    BASE_URL,
    NEWS_API_KEY,
    DEFAULT_QUERY,
    MAX_PAGES,
    PAGE_SIZE,
    ARTICLE_STORE_BASE,
    LOG_DIR
)


QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")
logger = get_logger("fetch_news")

#Making sure we have the necessary directories before we run the code
def ensure_directories():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

#Fetching the articles from News API
def fetch_article(query=DEFAULT_QUERY):
    #Declared a all articles list to store the articles   
    all_articles = []

    #Loopin through the pages and getting articles
    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": query,
            "pageSize": PAGE_SIZE,
            "page": page,
            "apiKey": NEWS_API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params)
            logger.info(f"Fetching page {1} -> {response.status_code} -> {response.url}")
            response.raise_for_status()
            
            #Converting the api data into JSON format
            data = response.json()

            if "articles" in data:
                #Writing to our all articles List
                all_articles.extend(data["articles"])
                logger.info(f"Page {page}: Retrieved {len(data["articles"]) } articles")
            
            else:
                logger.warning(f"Page {page}: No 'articles' key in resposne")
        
        except Exception as e:
            logger.error(f"Error fetching page {page} : {e}")
    return all_articles

#Saving each article locally and into their own folders

def save_article(article, index, total):
    #Creating a uuid( universally unique identifier) for each article
    article_id = str(uuid.uuid4())
    
    #Adding article fetched time and date and the  created article_id
    article["fetched_at"] = datetime.now(timezone.utc).isoformat()
    article["article_id"] = article_id

    logger.info(f"Processing article {index}/{total}: {article.get("title", "Untitled")}")

    #Creating a new folder for each article with their article_id
    folder_path = os.path.join(QUEUE_DIR, article_id)
    os.makedirs(folder_path, exist_ok=True)

    #Downloading and adding image to thearticle folder
    logger.info(f"Downloading image for article {article_id}")
    image_path = handle_aricle_image(article.get("urlToImage"), folder_path, article_id)
    article["article_image_original"] = image_path.replace("\\", "/")

    json_path = os.path.join(folder_path, f"{article_id}.json")

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved article {article_id} to {json_path}")
    except Exception as e:
        logger.error(f"Error saving article {article_id} : {e}")

def main():
    ensure_directories()
    print("Fetching articles from NewsAPI...")
    logger.info(f"Starting fetch for query: '{DEFAULT_QUERY}'")

    articles = fetch_article()
    logger.info(f"Total fetched: {len(articles)}")
    print(f"Total articles fetched: {len(articles)}")

    for idx, article in enumerate(tqdm(articles, desc="Saving articles..."), start=1):
        if article.get("title") and article.get("url"):
            save_article(article, idx, len(articles))
        else:
            logger.warning(f"Article at index {idx} missing title or url. Skipping...")
          
if __name__ == "__main__":
    main()

