import json, os
import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model

#https://newsapi.org/v2/everything?q=bitcoin&apiKey=API_KEY

NEWS_API_URL = "https://newsapi.org/v2/everything"
API_KEY = "b566af77a35141dca681d9db6e681d32"
HEADLINE_COUNT = 5 
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
        "q": "bitcoin",
        "pageSize": count
    })

    news_api_response.raise_for_status()
    news_articles = news_api_response.json().get("articles", [])
    logging.info(f"Fetched {len(news_articles)} articles")
    return news_articles

def generate_headlines(prompt,count=5):
    news_headline_tokens = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = gen_model.generate(
        news_headline_tokens,
        num_return_sequences = 5,
        max_new_tokens = 20,
        do_sample = True,
        temperature = 0.8,
        top_k = 50,
        top_p = 0.95
    )

    clean_headlines = []
    seen = set()
    for output in outputs:
        decoded = tokenizer.decode(output, skip_special_tokens=True).replace(prompt, "").strip()
        # Keep only first line before any newline or special characters
        headline = decoded.split("\n")[0].strip()
        if headline and headline not in seen:
            seen.add(headline)
            clean_headlines.append(headline)

        if len(clean_headlines) == count:
            break

    return clean_headlines


def process_news_articles(news_articles):
    # Get Each News Article and get Top 3 Headlines
    processed_articles = []

    for id, news_article in enumerate(news_articles):
        content = news_article.get("content") or ""
        title = news_article.get("title") or ""
        description = news_article.get("description") or ""

        # news_text = title + description + content
        news_text = f"{title}. {description}. {content}".strip()
        if not news_text:
            continue

        # Prepare prompt to get the headlines for each article
        prompt = f"Generate a headline for this news: \n{news_text}\nHeadline:"
        headline_candidates = generate_headlines(prompt)

        # Get the original prompt embeddings
        news_text_embedding = get_mean_embedding(prompt)

        result = []
        for headline in headline_candidates:
            headline_embedding = get_mean_embedding(headline)
            score = F.cosine_similarity(headline_embedding, news_text_embedding).item()
            result.append({"text": headline, "score": score})

        # Sort top headlines
        result.sort(key=lambda x: x["score"], reverse=True)

        #Get the top 5 headlines
        top_headlines = [
            {"score": idx + 1, "text": item["text"]}
            for idx, item in enumerate(result[:5])
        ]

        # Prepare structured article with top headlines
        article_data = {
            "source": news_article.get("source", {}),
            "author": news_article.get("author"),
            "title": title,
            "description": description,
            "url": news_article.get("url"),
            "urlToImage": news_article.get("urlToImage"),
            "publishedAt": news_article.get("publishedAt"),
            "content": content,
            "headlines": top_headlines  # All sorted headline suggestions with score
        }

        processed_articles.append(article_data)

        # Logging & Printing
        best = result[0]
        print("\n" + "="*60)
        print(f"ARTICLE #{id + 1}")
        print(f"Title: {title}")
        print(f"Generated Headline: {best['text']}")
        print(f"Semantic Similarity Score: {best['score']:.4f}")
        print("="*60 + "\n")

    # Final return
    return {
        "status": "ok",
        "totalResults": len(processed_articles),
        "articles": processed_articles
    }


def save_json(data, filename = "zpuv_vivek_ullengula_response.json"):

    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok = True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved the output to the file {filename}")
    

if __name__ == "__main__":
    articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
    processed_article_data = process_news_articles(articles)
    save_json(processed_article_data)

