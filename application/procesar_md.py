# application/procesar_md.py
from domain.document_chunk import DocumentChunk
from adapters.embedding.embedding_openai import get_embedding

def partir_md_en_chunks(texto: str, max_chars: int = 1000) -> list[DocumentChunk]:
    chunks = []
    for i in range(0, len(texto), max_chars):
        parte = texto[i:i+max_chars]
        embedding = get_embedding(parte)
        chunks.append(DocumentChunk(texto=parte, embedding=embedding))
    return chunks