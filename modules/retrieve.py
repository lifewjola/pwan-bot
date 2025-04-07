import streamlit as st
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from huggingface_hub import login

hf_token = st.secrets["HF_TOKEN"]

login(token=hf_token)

@st.cache_resource(show_spinner=False)
def get_vector_store():
    embeddings = FastEmbedEmbeddings()
    
    QDRANT_URL= st.secrets["QDRANT_URL"]
    QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    collection_name = "test"
    if not client.collection_exists(collection_name):
         st.error("Collection does not exist. Please upsert documents first.")
         return None, None, None, None
         
    vector_store = QdrantVectorStore(
         client=client,
         collection_name=collection_name,
         embedding=embeddings
    )
    return client, collection_name, embeddings, vector_store

client, collection_name, embeddings, vector_store = get_vector_store()

def retrieve_documents(query, k=5):
    if vector_store is None:
         return "Vector store is not available."
    embedding_vector = embeddings.embed_query(query)
    docs = vector_store.similarity_search_by_vector(embedding_vector, k=k)
    if not docs:
         st.error("No documents retrieved for the query.")
         return ""
    return "\n\n".join(doc.page_content for doc in docs)
