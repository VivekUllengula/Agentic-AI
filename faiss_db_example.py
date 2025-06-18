from openai import OpenAI
import numpy as np
import pickle
import faiss
import os

#config 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX = "text_index.faiss" #faiss db
LABEL_MAP_FILE = "text_index.pk1" #pickle
VECTOR_DIM = 1536

#Inti Open AI GPT4 Client
client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

#Creating FAISS index file
if os.path.exists(FAISS_INDEX):
    index = faiss.read_index(FAISS_INDEX) #Using existing Index
else:
    index = faiss.IndexFlatL2(VECTOR_DIM) #Creating new  Index

#Creating or Init Pickle file
if os.path.exists(LABEL_MAP_FILE):
    with open (LABEL_MAP_FILE, 'rb') as f:
        label_map = pickle.load(f)
else:
    label_map = {} 

#Getting the embeddings for the input text
def get_embeddings(text: str) -> list:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding #Return final embedding

def add_to_index():
    text = input("Enter text to add to faiss DB(index): ") #text = How are you Name
    label = input(f"Enter lable for {text}: ") #lable = Name

    text_embeddings = get_embeddings(text) #Get embeddings for text
    vector = np.array([text_embeddings]).astype("float32") #Convert embeddings to float32 type
    index_id = index.ntotal # Current size of total vectors
    index.add(vector) # Add to Index (FAISS DB) ->  Float32 ->  Embeddings -> Vector
    label_map[index_id] = label
    save_index()

def save_index(): #Saving the index to local DB - FAISS DB
    faiss.write_index(index, FAISS_INDEX)
    with open (LABEL_MAP_FILE, 'wb') as f:
        pickle.dump(label_map, f)

def list_labels():
   for idx,label in label_map:
       print(f"{idx} Lable - {label}")
       
def main():
    add_to_index()

if __name__ == "__main__":
    main()