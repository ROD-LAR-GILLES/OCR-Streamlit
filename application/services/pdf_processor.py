# domain/pdf_processor.py

import os
from pathlib import Path
import fitz
import pdfplumber
import pytesseract
import camelot
from pdf2image import convert_from_path
from tabulate import tabulate
from markitdown import MarkItDown
from stqdm import stqdm
from infrastructure.config.config import CUSTOM_CONFIG, RESULTADO_DIR

class PDFProcessor:
    def __init__(self, ocr_config=CUSTOM_CONFIG):
        self.ocr_config = ocr_config

    def extraer_texto(self, ruta_pdf: str) -> str:
        texto = ""
        doc = fitz.open(ruta_pdf)
        for idx in stqdm(range(doc.page_count), desc="Extrayendo texto/OCR"):
            page = doc[idx]
            contenido = page.get_text().strip()
            if not contenido:  # OCR si no hay texto
                imgs = convert_from_path(ruta_pdf, first_page=idx+1, last_page=idx+1, dpi=300)
                for img in imgs:
                    contenido += pytesseract.image_to_string(img, lang="spa", config=self.ocr_config)
            texto += contenido + "\n\n"
        return texto

    def extraer_tablas(self, ruta_pdf: str) -> str:
        tablas_md = ""
        # Camelot
        try:
            tablas = camelot.read_pdf(ruta_pdf, pages="all")
            for i, t in enumerate(tablas, 1):
                tablas_md += f"\n### Tabla {i} (Camelot)\n\n{t.df.to_markdown()}\n"
        except Exception:
            pass
        # pdfplumber
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    tbs = page.extract_tables()
                    for j, tb in enumerate(tbs, 1):
                        tablas_md += f"\n### Tabla {j} pág {i} (pdfplumber)\n\n{tabulate(tb, tablefmt='pipe')}\n"
        except Exception:
            pass
        return tablas_md

    def procesar_documento(self, ruta_pdf: str) -> str:
        os.makedirs(RESULTADO_DIR, exist_ok=True)
        name = Path(ruta_pdf).stem
        md_path = os.path.join(RESULTADO_DIR, f"{name}_completo.md")

        stqdm.write("Procesando con MarkItDown…")
        md_result = MarkItDown(enable_plugins=False).convert(ruta_pdf)

        texto = self.extraer_texto(ruta_pdf)
        tablas = self.extraer_tablas(ruta_pdf)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n## Contenido MarkItDown\n\n{md_result.text_content}\n")
            f.write(f"\n## Texto (PyMuPDF/OCR)\n\n{texto}\n")
            if tablas:
                f.write(f"\n## Tablas\n{tablas}\n")
        return md_path