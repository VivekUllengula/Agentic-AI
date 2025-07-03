import os, json, shutil
from tqdm import tqdm
from utils.logger import get_logger
from openai import OpenAI

ARTICLE_STORE_BASE = os.getenv("ARTICLE_STORE_BASE", "article_store")
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")
INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger = get_logger("reword_logger")

client = OpenAI(api_key= OPENAI_API_KEY)


def process_aticle(article_id):
    source_path = os.path.join(QUEUE_DIR, article_id)
    dest_path = os.path.join(INPROGRESS_DIR, article_id)
    shutil.move(source_path, dest_path)

    article_path = os.path.join(dest_path, f"{article_id}.json")
    
    if not os.path.exists(article_path):
       logger.warning("Article does not exists - {article_path}")
       shutil.move(dest_path, os.path.join(FAILED_DIR, article_id))
    try:
        with open (article_path, "r", encoding="utf-8") as f:
            article_data = json.load(f)
            
            title = article_data.get("title", "").strip()
            description = article_data.get("description", "").strip()
            content = article_data.get("content", "").strip()

            if not any ([title, description, content]):
                raise ValueError("Missing required fields")
            
            article_data["reworded_title"] = reword_text("Paraphrase this article title in a cleaner and more engaging way", title)
            article_data["reworded_description"] = reword_text("Paraphrase this article description that briefs on title", description)
            article_data["reworded_content"] = reword_text("Paraphrase this article content without losing meaning and in an engaging way", content)

            final_path = os.path.join(COMPLETED_DIR, article_data)
            os.makedirs(final_path, exist_ok=True)
            #shutil.move()
            with open(os.path.join(final_path, "f{article_id}.json"), "w", encoding="utf-8") as f:
                json.dump(article_data, f, indent=2)

    except Exception as e:
        logger.error(str(e))

def reword_text(prompt, content):
    response = client.chat.completions.create(
        model="gpt-4",
        messages= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    response.choices[0].message.content.strip()

def main():
    create_or_use_dirs()
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]

    for article_id in tqdm(article_folders, desc="Rewording articles"):
        process_aticle(article_id)


def create_or_use_dirs():
    os.makedirs(INPROGRESS_DIR, exist_ok=True)
    os.makedirs(COMPLETED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

if __name__ == "__main__":
    main()