# domain/pdf_processor.py

import fitz
import pdfplumber
import pytesseract
import camelot
from pathlib import Path
from pdf2image import convert_from_path
from tabulate import tabulate
from stqdm import stqdm
import os

class PDFProcessor:
    def __init__(self, ocr_config: str = r"--oem 3 --psm 6"):
        self.ocr_config = ocr_config

    def extraer_texto(self, ruta_pdf: str) -> str:
        texto = ""
        doc = fitz.open(ruta_pdf)
        for idx in stqdm(range(doc.page_count), desc="Extrayendo texto/OCR"):
            page = doc[idx]
            contenido = page.get_text().strip()
            if not contenido:  # OCR si no hay texto
                imgs = convert_from_path(ruta_pdf, first_page=idx + 1, last_page=idx + 1, dpi=300)
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