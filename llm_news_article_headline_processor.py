import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "fd5dd9059e6c423ab6d91ea447f2e72d"
HEADLINE_COUNT =3  
ARTICLE_COUNT = 5

logging.basicConfig(level=logging.INFO, format= "%(asctime)s - %(levelname)s -%(message)s")

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

#Adding padding tokens
tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors='pt')
    with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
    return embeddings.last_hidden_state.mean(dim=1)

def fetch_news_articles(api_key, count) -> list[dict]:
    logging.info("Fetching news articles.....Please wait")
    news_api_response = requests.get(NEWS_API_URL, params={
        "apiKey": api_key,
        "country": "us",
        "pageSize": count
    })

    news_api_response.raise_for_status()
    news_articles = news_api_response.json().get("articles", [])
    logging.info(f"Fetched {len(news_articles)} articles")
    return news_articles

def generate_headlines(prompt):
    news_headline_tokens = tokenizer(prompt, return_tensors="pt").input_ids
    headlines = gen_model.generate(
        news_headline_tokens,
        num_return_sequences = 1,
        max_new_tokens = 50,
        do_sample = True,
        temperature = 0.8,
        top_k = 50,
        top_p = 0.95
    )

    return [tokenizer.decode(headline, skip_special_tokens = True).replace(prompt, "").strip() for headline in headlines]


def process_news_articles(news_articles):

    #Get Each News Article and get Top 3 Headlines

    for id, news_article in enumerate(news_articles):
        content = news_article.get("content") or ""
        title = news_article.get("title") or ""
        description = news_article.get("description") or ""

        #news article = "title + description + content"

        news_text = f"{title}. {description}. {content}".strip()

        if not news_text:
            continue

        #Prepare Prompt to get the headlines for each article
        prompt = f"Generate a headline for this news: \n {news_text} \n Headline:"
        headline_candidates = generate_headlines(prompt)

        #get the original prompt embeddings
        news_text_embedding = get_mean_embedding(prompt)

        result = []

        for headline in headline_candidates:
            headline_mean_embedding = get_mean_embedding(headline)
            score = F.cosine_similarity(headline_mean_embedding, news_text_embedding).item()
            result.append((headline, score))

        best_headline, score = max(result, key = lambda x: x[1])
        print("\n" + "="*60)
        print(f"ARTICLE #{id + 1}")
        print(f"Title: {title}")
        print(f"Generated Headline: {best_headline}")
        print(f"Semantic Similarity Score: {score:.4f}")
        print("="*60 + "\n")


if __name__ == "__main__":
    articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
    process_news_articles(articles)

