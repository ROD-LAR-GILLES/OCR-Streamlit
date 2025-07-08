# adapters/embedding/embedding_openai.py
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    a, b = np.array(vec1), np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))