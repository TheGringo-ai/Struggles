# tools/retrieval.py

import os
import faiss
import pickle
from openai import OpenAI
from tools.embedding import get_embedding  # Assumes you have a helper here or inlined

INDEX_PATH = "tools/vector_index/faiss.index"
DOCS_PATH = "tools/vector_index/docs.pkl"

def retrieve_documents(query: str, k: int = 5) -> list[str]:
    """
    Retrieves relevant documents using vector search (FAISS + OpenAI).
    
    Args:
        query (str): The query string to retrieve documents for.
        k (int): Number of top documents to return.
    
    Returns:
        list[str]: A list of document texts relevant to the query.
    """
    print(f"[Retrieval] Looking up documents for query: '{query}'")

    # Load FAISS index and corresponding docs
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)

    index = faiss.read_index(INDEX_PATH)
    query_vector = get_embedding(query)  # Should return a list[float] of 1536-d

    D, I = index.search([query_vector], k)
    results = [documents[i] for i in I[0]]

    print(f"[Retrieval] Top results:\n" + "\n---\n".join(results))
    return results