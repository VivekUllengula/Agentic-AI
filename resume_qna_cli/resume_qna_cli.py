import os
import faiss
import numpy as np
import fitz
from openai import OpenAI
from pymongo import MongoClient

# -------------------- Configuration --------------------
PDF_FOLDER = "resumes"
FAISS_INDEX_FILE = "resume_index.faiss"
INDEX_DATA_FILE = "resume_chunks.npy"
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ameet:eyqKJ3E3b7ie2OFA@resumestore.c6xamui.mongodb.net/")
DB_NAME = "resume_manager"
COLLECTION_NAME = "resumes"
OPENAI_API_KEY = os.getenv ("OPENAI_API_KEY")
TEXT_EMBEDDINGS_MODEL = "text-embedding-ada-002"
 
# -------------------- Initalisation --------------------
openai_client = OpenAI  (api_key=OPENAI_API_KEY )
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
resume_collection = db[COLLECTION_NAME]
embedding_dim = 1536
index = faiss.IndexFlatL2(embedding_dim) # faiss
index_data = []

def load_index():
    if os.path.exists (FAISS_INDEX_FILE):
        global index, index_data  
        index = faiss.read_index(FAISS_INDEX_FILE)
    if os.path.exists(INDEX_DATA_FILE):
        index_data = np.load(INDEX_DATA_FILE, allow_pickle= True).tolist()

def load_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in pdf_document]) 
 
def chunk_text (text, chunk_size=500):
    words = text.split()
    return [ " ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def get_openai_embeddings(text):
    response = openai_client.embeddings.create(
        model = TEXT_EMBEDDINGS_MODEL,
        input =  text
    )
    return response.data[0].embedding
    
def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    np.save(INDEX_DATA_FILE, index_data) # Mapping

def index_resumes():
    global index_data
    for filename in os.listdir (PDF_FOLDER):
        if filename.endswith(".pdf"):
            if resume_collection.find_one({"_id": filename }):
                print (f"Skipping : {filename} - already indexed")
                continue

            text = load_pdf_text (os.path.join(PDF_FOLDER, filename))
            chunks = chunk_text (text)
            for chunk in chunks:
                embedding = get_openai_embeddings (chunk)
                index.add(np.array([embedding], dtype="float32"))
                index_data.append({"_id" : filename, "chunk" : chunk})
                resume_collection.insert_one({"_id" : filename, "text" : text})
            print (f"Indexed the resume {filename}")
    save_index()

def query_resume (query):
    return True
    # if index.ntotal ==0 or len (index_data) ==0:
    #     print ("No resumes are indexed. Please Use Option 1 ")
    #     return
    # query_vector = get_openai_embeddings (query)
    # X, I = index.search (np.array([query_vector], dype ="float32"),3) # Extract Chunk
    
    # context = []
    # for i in I [0]:

    


# Main - Implementation

def main():
    load_index()
    print (index_data)
    while True:
        print ("\n GPT4 Based Resume QNA")
        print ("1. Process the Resumes in Resume Folder")
        print ("2. Ask Questions")
        print ("3. Exit")
        choice = input ("Select an Option : ")

        if choice == "1":
            index_resumes()
        elif choice == "2":
            query = input ("Ask you question : ")
            query_resume (query)
        elif choice == "3":
            print ("Goodbye..... See you again.")
            break
        else:
            print ("Invalid user input. Please try again")


if __name__ == "__main__":
    main()
