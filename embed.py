import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

import spacy

nlp = spacy.load('en_core_web_sm')

def chunk_text(text, chunk_size=500):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    chunks = [' '.join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]
    return chunks

from openai import AzureOpenAI
from dotenv import load_dotenv 
import os
load_dotenv()
client = AzureOpenAI(
  api_key = os.getenv("AZURE_API_KEY"),  
  api_version = os.getenv('AZURE_API_VERSION'),
  azure_endpoint =os.getenv('AZURE_API_BASE_PATH')
)

def get_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embed-ada-east-us2" 
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

import chromadb
from chromadb.utils import embedding_functions
storage_path=os.getenv("STORAGE_PATH")
chroma_client = chromadb.PersistentClient(path=storage_path)

collection = chroma_client.get_or_create_collection(
    name="pdf_embeddings"
)
def store_embeddings(text_chunks, embeddings):
    for i, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
        collection.add(ids=f"doc_{i}", documents=chunk, embeddings=embedding)

def similarity_search(query, top_k=5):
    query_embedding = get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results
def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    text_chunks = chunk_text(text)
    embeddings = get_embeddings(text_chunks)
    store_embeddings(text_chunks, embeddings)

pdf_path = 'venv/max-life-group-credit-life-secure-policy-document-v1.pdf'
process_pdf(pdf_path)
query = "Insurance"
results = similarity_search(query)
print(results)