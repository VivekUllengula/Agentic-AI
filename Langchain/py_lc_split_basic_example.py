#This is a program which will accept the long text and chunk into
# small parts and send each chunk to GPT4 & ask to summarize it.

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

os.environ["OPENAI_API_KEY"] = ""

#Step 1: Get the long text
long_text = """
LangChain is a powerful framework for building applications using language models. 
It offers tools to manage prompts, chains, memory, agents, and external tools.
This makes it easier to build complex LLM applications that interact with real-world data.
You can process documents, create chatbots, query databases, or even automate workflows.
"""

#chunk_overlap: Ensures context is preserved between chunks
#10 charcters from the end of one chunk is added to the next.
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 10,
    separators=["\n\n", ".", " ", "", "\n"]
)

#Step 2: Spli the text and get the chunks
chunks = splitter.split_text(long_text)

print(f" Total Lenght {len(chunks)} \n")

"""
0 : LangChain is a powerful framework for building
1 : building applications using language models
2 : .
It offers tools to manage prompts, chains,
3 : chains, memory, agents, and external tools
4 : .
This makes it easier to build complex LLM
5 : LLM applications that interact with real-world
6 : data
7 : .
You can process documents, create chatbots,
8 : chatbots, query databases, or even automate
9 : automate workflows
10 : .
"""

#Step 3: Send each chunk to GPT4 to summarize it.
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

prompt = PromptTemplate(
     input_variables= ["text"],
     template= "Summarize this chunk: \n{text}"
)

chain = LLMChain(llm = llm, prompt = prompt)

for i, chunk in enumerate(chunks):
    chunk_summary = chain.run({"text": chunk})
    print(f"\n ---Chunk {i+1} : {chunk} \n Summary is : {chunk_summary}")
