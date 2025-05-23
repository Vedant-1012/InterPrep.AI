"""
FAISS search integration for InterPrep-AI Next Generation.
"""
import numpy as np
import faiss
from .embeddings import generate_embeddings, generate_query_embedding

class FAISSIndex:
    """FAISS index for similarity search."""
    
    def __init__(self, dimension=384):
        """Initialize FAISS index."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.ids = []
        self.questions = []
    
    def add_questions(self, questions):
        """Add questions to the index."""
        # Extract embeddings
        embeddings = np.array([np.array(q['embedding']) for q in questions], dtype=np.float32)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store question IDs and data
        start_id = len(self.ids)
        for i, q in enumerate(questions):
            self.ids.append(q['id'])
            self.questions.append(q)
        
        return start_id, start_id + len(questions) - 1
    
    def search(self, query, k=5):
        """Search for similar questions."""
        # Generate query embedding
        if isinstance(query, str):
            query_embedding = generate_query_embedding(query)
        else:
            query_embedding = query
        
        # Reshape for FAISS
        query_embedding = np.array([query_embedding], dtype=np.float32)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Get results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.questions):
                question = self.questions[idx]
                results.append({
                    'question': question,
                    'distance': float(distances[0][i]),
                    'similarity': 1.0 / (1.0 + float(distances[0][i]))
                })
        
        return results
    
    def save(self, filepath):
        """Save the index to a file."""
        faiss.write_index(self.index, filepath)
    
    def load(self, filepath):
        """Load the index from a file."""
        self.index = faiss.read_index(filepath)

def create_question_index(questions):
    """Create a FAISS index for questions."""
    # Generate embeddings for questions
    from .embeddings import generate_question_embeddings
    questions_with_embeddings = generate_question_embeddings(questions)
    
    # Create index
    index = FAISSIndex()
    index.add_questions(questions_with_embeddings)
    
    return index

def search_questions(index, query, k=5):
    """Search for questions similar to the query."""
    return index.search(query, k)

from ..models import Question

# Global FAISS index (in-memory; not persistent)
faiss_index = None

def search_similar_questions(query, limit=5):
    """Search similar questions using FAISS index."""
    global faiss_index

    # Initialize index if not already done
    if faiss_index is None:
        questions = Question.query.filter(Question.embedding.isnot(None)).all()
        questions_data = [
            {
                'id': q.id,
                'title': q.title,
                'content': q.content,
                'embedding': q.embedding
            }
            for q in questions
        ]
        faiss_index = create_question_index(questions_data)
    
    # Search using FAISS
    results = search_questions(faiss_index, query, k=limit)
    return [r['question']['id'] for r in results]