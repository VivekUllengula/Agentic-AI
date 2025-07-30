from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader
import os

os.environ["OPENAI_API_KEY"] = ""

#Step 1: Load PDF file
pdf_path = "sample.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

pdf_text = "\n".join([page.page_content for page in pages])

#Step 2: Split into chunks

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50
)

chunks = splitter.split_text(pdf_text)

print(f"Total chunks are: {len(chunks)}")

#Step 3 : Init LLm and Setup Prompt Chain
llm = ChatOpenAI (model = "gpt-4", temperature=0.3)

prompt = PromptTemplate(
    input_variables=["text"],
    template= "Summarize this chunk: \n {text}"
)

chain = LLMChain(llm=llm, prompt=prompt)

for i, chunk in enumerate(chunks):
    chunk_summary = chain({"text": chunk})
    print (f"\n--- Chunk {i+1} : {chunk} \nSummary ---\n {chunk_summary}")