# domain/document_chunk.py
from dataclasses import dataclass

@dataclass
class DocumentChunk:
    texto: str
    embedding: list[float]