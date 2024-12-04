import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import shutil
load_dotenv()

def load_chunks(chunks:list):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        embedding_function = embeddings,
        persist_directory = "./chroma_store",
        collection_name = "test_collection"
    )
    print("Addng documents to vectorstore")
    vectorstore.add_documents(chunks)
    print("Documents added to vectorstore")

def retriver(question:str):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        embedding_function = embeddings,
        persist_directory = "./chroma_store",
        collection_name = "test_collection"
    )
    return vectorstore.as_retriever()
  #  docs = vectorstore.similarity_search(question, k=3)
  #  return docs

