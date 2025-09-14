import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from services.Classifier.src.config import *


class TextClassifier:
    def __init__(self):
        # Topic in Hebrew
        self.topics = [TOPICS]

        # Topics in english
        self.english_topics = [ENGLISH_TOPICS]

        # Loading the model
        print("טוען מודל...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("המודל נטען בהצלחה!")

    def classify_text(self, text):

        # creating an embeddings
        text_embedding = self.model.encode([text])
        topic_embeddings = self.model.encode(self.topics)

        # Similarity calculation
        similarities = cosine_similarity(text_embedding, topic_embeddings)[0]

        # Finding the most similar topic
        best_topic_idx = np.argmax(similarities)
        best_topic = self.english_topics[best_topic_idx]

        return {
            'category': best_topic,
            'text': text
        }
