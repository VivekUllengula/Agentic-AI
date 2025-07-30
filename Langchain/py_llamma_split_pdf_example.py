from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda

# Load PDF
loader = PyPDFLoader("sample.pdf")
pages = loader.load()
pdf_text = "\n".join([page.page_content for page in pages])

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(pdf_text)
print(f"Total chunks: {len(chunks)}")

# Load model & tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU (use `device=0` for GPU if available)
    max_new_tokens=256,
    temperature=0.3,
    do_sample=True,
    top_p=0.95
)

llm = HuggingFacePipeline(pipeline=pipe)

# Prompt
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize this chunk:\n{text}"
)

# New chain format
chain = prompt | llm | RunnableLambda(lambda x: x.strip())

# Run
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
    summary = chain.invoke({"text": chunk})
    print(f"\nSummary:\n{summary}")
