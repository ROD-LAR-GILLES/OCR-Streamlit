# application/chat_retrieval.py
from domain.document_chunk import DocumentChunk
from adapters.embedding.embedding_openai import cosine_similarity

def buscar_chunks_relevantes(chunks: list[DocumentChunk], pregunta: str, pregunta_embedding: list[float], top_k: int = 5):
    ordenados = sorted(
        chunks,
        key=lambda c: cosine_similarity(c.embedding, pregunta_embedding),
        reverse=True
    )
    return ordenados[:top_k]