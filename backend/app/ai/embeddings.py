"""
Embeddings generation using SentenceTransformer for InterPrep-AI Next Generation.
"""
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from ..config import Config

# Load the embedding model
model = None

def get_embedding_model():
    """Get or initialize the embedding model."""
    global model
    if model is None:
        model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)
    return model

def generate_embeddings(texts):
    """Generate embeddings for a list of texts."""
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def generate_question_embeddings(questions):
    """Generate embeddings for a list of questions."""
    # Extract question content
    texts = [f"{q['title']} {q['content']}" for q in questions]
    
    # Generate embeddings
    embeddings = generate_embeddings(texts)
    
    # Add embeddings to questions
    for i, q in enumerate(questions):
        q['embedding'] = embeddings[i].tolist()
    
    return questions

def generate_query_embedding(query):
    """Generate embedding for a search query."""
    model = get_embedding_model()
    embedding = model.encode(query, convert_to_numpy=True)
    return embedding

def embed_text(text):
    """Generate embedding for a single piece of text (compatibility wrapper)."""
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding