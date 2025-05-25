"""
Question retrieval service for InterPrep-AI.
"""
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from pathlib import Path



from pathlib import Path
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

from pathlib import Path

class QuestionRetriever:
    def __init__(self, csv_path=None, embedding_path=None):
        # Go from /backend/app/services → /backend → /interprep-ai-nextgen
        PROJECT_ROOT = Path(__file__).resolve().parents[3]  # ✅ This points to /interprep-ai-nextgen

        # This will now point to: /Users/vedantthakkar/Desktop/interprep-ai-nextgen/Data/final_preprocessed_data.csv
        self.csv_path = csv_path or str(PROJECT_ROOT / 'Data' / 'final_preprocessed_data.csv')
        self.embedding_path = embedding_path or str(PROJECT_ROOT / 'Data' / 'question_embeddings.npy')

        self.questions_df = None
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.load_dataset()
        self.load_or_create_embeddings()

    def load_dataset(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Dataset file not found: {self.csv_path}")
        self.questions_df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.questions_df)} questions from {self.csv_path}")

    def load_or_create_embeddings(self):
        if os.path.exists(self.embedding_path):
            try:
                self.embeddings = np.load(self.embedding_path)
                print(f"Loaded embeddings from {self.embedding_path}")
                if len(self.embeddings) != len(self.questions_df):
                    print("Embedding count doesn't match dataset size. Regenerating embeddings...")
                    self.create_embeddings()
            except Exception as e:
                print(f"Error loading embeddings: {str(e)}. Regenerating...")
                self.create_embeddings()
        else:
            self.create_embeddings()

    def create_embeddings(self):
        texts = [
            f"{row['Title']} {row['Topic']} {row['Difficulty']}" 
            for _, row in self.questions_df.iterrows()
        ]
        self.embeddings = self.model.encode(texts)
        os.makedirs(os.path.dirname(self.embedding_path), exist_ok=True)
        np.save(self.embedding_path, self.embeddings)
        print(f"Created and saved embeddings for {len(self.questions_df)} questions")

    def filter_questions(self, topic=None, difficulty=None, company=None, limit=10):
        filtered_df = self.questions_df.copy()
        if topic:
            filtered_df = filtered_df[filtered_df['Topic'].str.lower() == topic.lower()]
        if difficulty:
            filtered_df = filtered_df[filtered_df['Difficulty'].str.lower() == difficulty.lower()]
        if company:
            filtered_df = filtered_df[filtered_df['Company'].str.contains(company, case=False, na=False)]
        if limit and limit > 0:
            filtered_df = filtered_df.head(limit)
        return filtered_df.to_dict('records')

    def find_similar_questions(self, question_text, n=5, topic=None, difficulty=None, company=None):
        query_embedding = self.model.encode([question_text])[0]
        filtered_indices = list(range(len(self.questions_df)))
        if topic or difficulty or company:
            filtered_df = self.questions_df.copy()
            if topic:
                filtered_df = filtered_df[filtered_df['Topic'].str.lower() == topic.lower()]
            if difficulty:
                filtered_df = filtered_df[filtered_df['Difficulty'].str.lower() == difficulty.lower()]
            if company:
                filtered_df = filtered_df[filtered_df['Company'].str.contains(company, case=False, na=False)]
            filtered_indices = filtered_df.index.tolist()
        similarities = []
        for i in filtered_indices:
            if i < len(self.embeddings):
                similarity = np.dot(query_embedding, self.embeddings[i]) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(self.embeddings[i])
                )
                similarities.append((i, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        similar_indices = [idx for idx, _ in similarities[:n]]
        similar_questions = self.questions_df.iloc[similar_indices].to_dict('records')
        for i, q in enumerate(similar_questions):
            if i < len(similarities):
                q['similarity_score'] = float(similarities[i][1])
        return similar_questions

    def get_question_by_id(self, question_id):
        if 'ID' not in self.questions_df.columns:
            return None
        question = self.questions_df[self.questions_df['ID'] == question_id]
        if len(question) == 0:
            return None
        return question.iloc[0].to_dict()

    def get_random_question(self, topic=None, difficulty=None, company=None):
        filtered = self.filter_questions(topic, difficulty, company, limit=None)
        if not filtered:
            return None
        return filtered[np.random.randint(0, len(filtered))]

# Singleton instance
question_retriever = QuestionRetriever()

def filter_questions(topic=None, difficulty=None, company=None, limit=10):
    return question_retriever.filter_questions(topic, difficulty, company, limit)

def find_similar_questions(question_text, n=5, topic=None, difficulty=None, company=None):
    return question_retriever.find_similar_questions(question_text, n, topic, difficulty, company)

def get_question_by_id(question_id):
    return question_retriever.get_question_by_id(question_id)

def get_random_question(topic=None, difficulty=None, company=None):
    return question_retriever.get_random_question(topic, difficulty, company)