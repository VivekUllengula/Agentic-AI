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

#Making sure that all the directories are present if not create them
def create_or_use_dirs():
    os.makedirs(INPROGRESS_DIR, exist_ok=True)
    os.makedirs(COMPLETED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

#Using GPT4 to reword the text
def reword_text(prompt, content):
    try:
        response = client.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"OpenAI error during rewording: {e}")
        return None

#Processing each article in the queue folder
def process_article(article_id):
    source_path = os.path.join(QUEUE_DIR, article_id)
    working_folder = os.path.join(INPROGRESS_DIR, article_id)

    try:
        shutil.move(source_path, working_folder)
    except Exception as e:
        logger.error(f"Failed to move article {article_id} to inprogress folder: {e}")
        return

    article_path = os.path.join(working_folder, f"{article_id}.json")
    
    if not os.path.exists(article_path):
        logger.warning(f"Article file does not exist: {article_path}")
        shutil.move(working_folder, os.path.join(FAILED_DIR, article_id))
        return
    
    #Reword Title, Description & Content inside Json File
    try:
        with open(article_path, "r", encoding="utf-8") as f:
            article_data = json.load(f)

        #Getting the Title, Description & Content from JSON file
        title = article_data.get("title", "").strip()
        description = article_data.get("description", "").strip()
        content = article_data.get("content", "").strip()

        if not any([title, description ,content]):
            raise ValueError("Missing required fields")
        
        #Adding the reworder text as new keys into the JSON file
        article_data["reworded_title"] = reword_text("Reword this article title in a cleaner and more engaging way:", title)
        article_data["reworded_description"] = reword_text("Rephrase this article description to be concise and original:", description)
        article_data["reworded_content"] = reword_text("Rewrite this content in your own words without losing meaning:", content)

        dest_path = os.path.join(COMPLETED_DIR, article_id)
        os.makedirs(dest_path, exist_ok=True)

        #Copying from Inprogress to final completed folder
        shutil.copytree(working_folder, dest_path, dirs_exist_ok=True)

        #Writing the updated article JSON file in the completed folder
        with open(os.path.join(dest_path, f"{article_id}.json"), "w", encoding="utf-8") as f:
            json.dump(article_data,f, indent=2, ensure_ascii=False)

        #Deleting the files from Inprogress folder
        shutil.rmtree(working_folder)
        logger.info(f"Completed: {article_id}") 
    
    except Exception as e:
        logger.error(f"Processing failed for {article_id}: {e}")
        shutil.move(working_folder, os.path.join(FAILED_DIR, article_id))

#Sending each article to process
def main():
    create_or_use_dirs()
    
    #Getting the names of each article folder from Queue Folder
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]

    print(f"{len(article_folders)} articles available to process.")

    for article_id in tqdm(article_folders, desc="Rewording articles..."):
        process_article(article_id)

if __name__ == "__main__":
    main()