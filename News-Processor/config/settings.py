import os

BASE_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "b566af77a35141dca681d9db6e681d32"
DEFAULT_QUERY = "bitcoin"
MAX_PAGES = 1
PAGE_SIZE = 5
QUEUE_DIR = "queue"
LOG_DIR = "logs"
ARTICLE_STORE_BASE = "article_store"
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")