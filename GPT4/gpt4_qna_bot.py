import fitz
import os
import openai
import numpy as np
import faiss

CHUNK_SIZE = 500
EMBED_MODEL = "text-embedding-3-small"
INDEX_FILE_PATH = "faiss.index"

index = None
chunk = []

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def embed_chunks(text_chunks):
    embeddings = openai.embeddings.create(model=EMBED_MODEL, input=text_chunks)
    vectors = np.array([e.embedding for e in embeddings.data]).astype("float32")
    return vectors

def chunk_text(text):
    words = text.split()
    return [ " ".join(words[i: i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]

def extract_text_from_pdf(pdf_path):
    pages = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in pages])
    return full_text

def add_document():
    global index, chunk
    pdf_path = input("Enter path for PDF File: ").strip()
    if not os.path.exists(pdf_path):
        print(f"File not found at location {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path) 

    if not text:
        print("No content found. Try another PDF file")
        return
    
    text_chunks = chunk_text(text)
    vectors = embed_chunks(text_chunks)

    chunk = text_chunks  # Important to keep reference for search
    
    index = faiss.IndexFlatL2(vectors.shape[1]) #Inmemeory Index
    index.add(vectors)
    faiss.write_index(index, INDEX_FILE_PATH)
    print("Document was indexed successfully")

def search_faiss_index(query_vector, index):

    distance, indices = index.search(query_vector, 5)
    return indices[0]

def ask_gpt4(context, query):
    context = "\n".join(context)
    system_prompt = (
        "You are an expert assistant. Answer only based on the provided context."
        "If the answer is not found then say no information available"
    )

    messages = [
        {"role": "system", "content": system_prompt },
        {"role": "user", "content": f"Context: \n {context}\n Question: {query}" }
    ]

    response = openai.chat.completions.create(
        model = "gpt-4",
        messages= messages,
        temperature = 0.2
    )

    return response.choices[0].message["content"]

def query_document():
    query = input("Please enter your query or questions to search the Index")
    query_embedding = openai.embeddings.create(model = EMBED_MODEL, input = query)
    query_vectors = np.array([e.embedding for e in query_embedding.data]).astype("float32")
    
    top_indices = search_faiss_index(query_vectors, index)
    context = [chunk[i] for i in top_indices]
    answer = ask_gpt4(context, query)
    print(f"\nAnswer for question {query} is: {answer}")

def delete_document():
    return True

def main():
    #1.Add Doc to Faiss Index
    #2.Query Doc
    #3.Del Doc
    #4.Exit

    while True:
        print("\n Select an option: ")
        print("1.Add Doc to Faiss Index")
        print("2.Query Document")
        print("3.Delete Dcoument")
        print("4.Exit")

        choice = input("Please select and option. (1/2/3/4) ").strip()

        if choice == "1":
            add_document()
        elif choice =="2":
            query_document()
        elif choice =="3":
            delete_document()
        elif choice == "4":
            print("Goodbye - See you again")
            break
        else:
            print("Incorrect choice. Please try again")                    
if __name__ == "__main__":
    main()