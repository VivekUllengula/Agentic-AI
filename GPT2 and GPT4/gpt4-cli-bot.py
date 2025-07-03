import os
import sys
import faiss
import openai
import numpy as np
import fitz
import logging
from dotenv import load_dotenv

CHUNK_SIZE = 500
EMBEDDING_MODEL = 'text-embedding-3-small'
#Step - 1 
load_dotenv() #-> Load the Env Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

#pdf_file_path = r"C:\Users\svcs\Desktop\python fast api.pdf"

#Step 2 -> Setup Logging
logging.basicConfig(
    filename="cli_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger = logging.getLogger(__name__)

#Step 3 -> Read PDF file
def extract_text_from_pdf(pdf_file_path):
    try:
        pdf_pages = fitz.open(pdf_file_path)
        full_pdf_text = " \n".join([page.get_text() for page in pdf_pages])
        logger.info(f" Extracted text from {pdf_file_path} with length of {len(full_pdf_text)}")
        return full_pdf_text
    except Exception as e:
        logger.exception(f"Failed to read text from {pdf_file_path}. Error is {e} ")

# Step 4 - Chunk the PDF Content based on Chunk Size (500) - Words 
def chunk_text(pdf_file_full_text, chunk_size):
    words = pdf_file_full_text.split()
    return [" ".join(words[i: i + chunk_size])for i in range(0, len(words), chunk_size)]

# Step 5 - Use EMBEDDING_MODEL and get the Embeddings, convert or cast to np float 32
def chunk_embedding(chunk_text):
    try:
        embeddings = openai.embeddings.create(model=EMBEDDING_MODEL, input=chunk_text)
        vectors = np.array( [ e.embedding for e in embeddings.data]).astype("float32")
        return vectors
    except Exception as e:
        logger.exception(f"Error while getting embeddings {e}")  
        sys.exit(1)    

def search_faiss_index(index, query_vector):
    distance, indices = index.search(query_vector, 5) #Search Data
    return indices[0]

def ask_gpt4(content_chunks, query):

    content = "\n".join(content_chunks)

    system_prompt = (
        "You are an expert assistant. Answer ONLY based on the provided context."
        "If the answer is not found, say 'No information available'"
    )  
    messages = [
        {"role": "system", "content" : system_prompt},
        {"role": "user", "content": f"Content: \n {content} \n Question {query}"},
    ]

    response = openai.chat.completions.create(
        model = "gpt-4",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
        
def main():

    if len(sys.argv) < 2:
        print("Usage : python gpt4-cli-bot.py <PDF File Path>")
        sys.exit(1)
    pdf_file_path = sys.argv[1] #Getting file path from cmd line arguments    

    pdf_text = extract_text_from_pdf(pdf_file_path)
    
    print (f"\n PDF Content are loaded and found  : {len(pdf_text)} ")
    
    chunked_text = chunk_text(pdf_text, CHUNK_SIZE)
    print ("\n Text from PDF is Chunked")

    vectors = chunk_embedding(chunked_text)
    print ("\n Obtained the Vector from the Chunked Text") 

    #Decalre a FAISS Index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    logger.info(f"Faiss Index Created......{len(chunked_text)}")

    while True:
        query = input("\n Please ask your question (type exit to close application)")
        if query.lower() == "exit":
            print("Goodbye")
            break;

        try:
            query_embeddig = openai.embeddings.create(model = EMBEDDING_MODEL, input = query)
            query_vector = np.array([query_embeddig.data[0].embedding], dtype='float32')
            top_indices = search_faiss_index(index, query_vector)
            context = [chunked_text[i] for i in top_indices]
            answer = ask_gpt4(context, query)
            print(f"\nAnswer : {answer}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()