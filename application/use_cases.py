import os
from pathlib import Path
from markitdown import MarkItDown
from application.chat_retrieval import chat_engine
from application.services.pdf_processor import PDFProcessor

RESULTADO_DIR = "data/resultado"
pdf_processor = PDFProcessor()

def procesar_documento(ruta_pdf: str) -> str:
    os.makedirs(RESULTADO_DIR, exist_ok=True)
    name = Path(ruta_pdf).stem
    md_path = os.path.join(RESULTADO_DIR, f"{name}_completo.md")

    md_result = MarkItDown(enable_plugins=False).convert(ruta_pdf)
    texto = pdf_processor.extraer_texto(ruta_pdf)
    tablas = pdf_processor.extraer_tablas(ruta_pdf)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n## Contenido MarkItDown\n\n{md_result.text_content}\n")
        f.write(f"\n## Texto (PyMuPDF/OCR)\n\n{texto}\n")
        if tablas:
            f.write(f"\n## Tablas\n{tablas}\n")
    return md_path

def list_markdowns() -> list[str]:
    return sorted([
        f for f in os.listdir(RESULTADO_DIR)
        if f.endswith("_completo.md")
    ], reverse=True) if os.path.isdir(RESULTADO_DIR) else []

def responder_pregunta(contenido: str, pregunta: str) -> str:
    prompt = f"Contexto:\n{contenido}\n\nPregunta: {pregunta}"
    return chat_engine.chat(prompt)