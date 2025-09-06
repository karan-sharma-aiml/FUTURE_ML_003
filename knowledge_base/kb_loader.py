from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pandas as pd, openai

def load_faqs():
    data = pd.read_csv("knowledge_base/faqs.csv")
    embeddings = OpenAIEmbeddings()
    docs = [f"Q: {q} A: {a}" for q, a in zip(data["question"], data["answer"])]
    vector_db = FAISS.from_texts(docs, embeddings)
    return vector_db
