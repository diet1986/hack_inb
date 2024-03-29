# -*- coding: utf-8 -*-
"""pinecone-db-langchain-working.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17zrBzl-y8gHOJq0O-asTj_W_lsb11XzS
"""

!pip install unstructured tiktoken pinecone-client pypdf openai langchain pandas numpy python-dotenv numpy tiktoken

import openai
import langchain
import pinecone
import pandas as pd
import numpy as np
import tiktoken
import re
import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone

## Lets Read the document
def read_doc(directory):
    file_loader=PyPDFDirectoryLoader(directory)
    documents=file_loader.load()
    return documents

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    docs=text_splitter.split_documents(docs)
    return docs

documents_from_folder=read_doc('documents/')
documents_chunked=chunk_data(docs=documents_from_folder)
len(documents_chunked)

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade --quiet  langchain-pinecone langchain-openai langchain

embeddings = OpenAIEmbeddings(openai_api_key='<openai_api_key>')

import time
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="<pinecone_api_key>")

spec = ServerlessSpec(cloud="aws", region="us-west-2")
index_name="langchain-test-index"

# check if index already exists (it shouldn't if this is your first run)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embed-3-small
        metric='cosine',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()

PINECONE_API_KEY='<pinecone_api_key>'

import os
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

from langchain_pinecone import PineconeVectorStore

docsearch = PineconeVectorStore.from_documents(documents_chunked, embeddings, index_name=index_name)

## Cosine Similarity Retreive Results from VectorDB
def retrieve_query(query,k=2):
    matching_results=docsearch.similarity_search(query,k=k)
    return matching_results

from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain_community.chat_models import ChatOpenAI

llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.5,openai_api_key="openai_api_key")
chain=load_qa_chain(llm,chain_type="stuff")
print(chain)

## Search answers from VectorDB
def retrieve_answers(query):
    doc_search=retrieve_query(query)
    print(doc_search)
    response=chain.run(input_documents=doc_search,question=query)
    return response

our_query = "what is the investment in new sub-scheme of PM Matsya Sampada?"
answer = retrieve_answers(our_query)
print(answer)