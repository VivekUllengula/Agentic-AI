import os, json, shutil, torch
from tqdm import tqdm
from utils.logger import get_logger
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Model

ARTICLE_STORE_BASE = os.getenv("ARTICLE_STORE_BASE", "article_store")
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")
INPROGRESS_DIR = os.path.join(ARTICLE_STORE_BASE, "inprogress")
COMPLETED_DIR = os.path.join(ARTICLE_STORE_BASE, "completed")
FAILED_DIR = os.path.join(ARTICLE_STORE_BASE, "failed")

logger = get_logger("reword_logger")

#Intializing the GPT2Tokenizer, GPT2LMHeadModel
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

#Adding padding tokens
tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

#Making sure that all the directories are present if not create them
def create_or_use_dirs():
    os.makedirs(INPROGRESS_DIR, exist_ok=True)
    os.makedirs(COMPLETED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors='pt')
    with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
    return embeddings.last_hidden_state.mean(dim=1)

def generate_with_gpt2(prompt, max_length = 150):
    try:
        inputs = tokenizer.encode(prompt, return_tensor="pt")
        outputs = gen_model.generate(
            inputs,
            max_lenght = max_length,
            pad_token_id = tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.8,
            top_k=50,
            top_p=0.95
        )
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated[len(prompt):].strip()
    except Exception as e:
        logger.error(f"GPT-2 generation failed: {e}")
        return None
    
def reword_field(field_type, text):
    prompt_map = {
        "title": "Rewrite this article title to make it more engaging:",
        "description": "Paraphrase the following article description to make it concise and original:",
        "content": "Rewrite the article content below in simpler and clearer terms:"
    }
    prompt = prompt_map.get(field_type, "Rewrite the following text:")
    return generate_with_gpt2(f"{prompt}\n\n{text}")

def process_article(article_id):
    source_path = os.path.join(QUEUE_DIR, article_id)
    working_path = os.path.join(INPROGRESS_DIR, article_id)
    completed_path = os.path.join(COMPLETED_DIR, article_id)
    failed_path = os.path.join(FAILED_DIR, article_id)

    try:
        shutil.move(source_path, working_path)
    except Exception as e:
        logger.error(f"Failed to move article {article_id} to inprogress: {e}")
        return
    
    article_json_path = os.path.join(working_path, f"{article_id}.json")

    if not os.path.exists(article_json_path):
        logger.warning(f"Missing JSON: {article_json_path}")
        shutil.move(working_path, failed_path)
        return

    try:
        with open(article_json_path, "r", encoding="utf-8") as f:
            article_data = json.load(f)

        title = article_data.get("title", "")
        description = article_data.get("description", "")
        content = article_data.get("content", "")

        if not any([title, description, content]):
            raise ValueError("Missing title, description, or content")

        # Reword each field
        article_data["reworded_title"] = reword_field("title", title)
        article_data["reworded_description"] = reword_field("description", description)
        article_data["reworded_content"] = reword_field("content", content)

        os.makedirs(completed_path, exist_ok=True)
        shutil.copytree(working_path, completed_path, dirs_exist_ok=True)

        # Save updated JSON
        with open(os.path.join(completed_path, f"{article_id}.json"), "w", encoding="utf-8") as f:
            json.dump(article_data, f, indent=2, ensure_ascii=False)

        shutil.rmtree(working_path)
        logger.info(f"Reworded and completed article: {article_id}")

    except Exception as e:
        logger.error(f"Error processing article {article_id}: {e}")
        shutil.move(working_path, failed_path)

def main():
    create_or_use_dirs()
    article_folders = [name for name in os.listdir(QUEUE_DIR) if os.path.isdir(os.path.join(QUEUE_DIR, name))]

    print(f"{len(article_folders)} articles available to reword.")
    for article_id in tqdm(article_folders, desc="Rewording articles"):
        process_article(article_id)


if __name__ == "__main__":
    main()      