
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from chromadb_service import retriver, load_chunks
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def load_chunks(docs):
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

#chatgpt model selection
LLM = ChatOpenAI(model="gpt-4o-mini")
retriver = retriver()
#Template declaeation
prompt = ChatPromptTemplate.from_template(
    """You can answer any question from this data {data}.
    This is the topic: {question}"""
)

#piping i.e output of promt is input for LLM
chain = (
     {"data": retriver() | format_docs, "question": RunnablePassthrough()}
     | prompt
     | LLM
     | StrOutputParser()
)
#invoking questions
#print(chain.invoke({"question":"dogs"}))

response = chain.stream({"question":"dogs"})
for r in response:
    print(r, end="", flush=True)
