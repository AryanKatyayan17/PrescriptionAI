import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

df=pd.read_csv('data/patient_records.csv')
documents=[Document(page_content=row["record"],metadata={"patient_id":row["patient_id"]}) for _,row in df.iterrows()]

splitter=RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)
split_docs=splitter.split_documents(documents)

embedding_model=OpenAIEmbeddings()
vectorstore=FAISS.from_documents(split_docs,embedding_model)

vectorstore.save_local("vector_store/patient_records_index")
print("FAISS vectorstore built and saved")