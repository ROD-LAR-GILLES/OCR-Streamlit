#!/usr/bin/env python
# interfaces/streamlit/streamlit_app.py
import os
from pathlib import Path
import fitz                
import pdfplumber
import pytesseract
import camelot
from pdf2image import convert_from_path
from tabulate import tabulate
from markitdown import MarkItDown

from openai import OpenAI
import streamlit as st
from stqdm import stqdm
from dotenv import load_dotenv

# =========================
#  CONFIGURACIÓN GLOBAL
# =========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CUSTOM_CONFIG = os.getenv("TESSERACT_CONFIG", r"--oem 3 --psm 6")
PDF_DIR = "data/pdfs"
RESULTADO_DIR = "data/resultado"

# =========================
#  MODELO LLM (OpenAI)
# =========================
class OpenAIChat:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def chat(self, prompt: str) -> str:
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de documentos."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()

chat_engine = OpenAIChat()

# =========================
#  PROCESADOR DE PDF
# =========================
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

pdf_processor = PDFProcessor()

# =========================
#  USUARIOS DEMO / LOGIN
# =========================
USERS = {"admin": "password", "user": "passuser", "guest": "guestpass"}
def check_login(u, p): return USERS.get(u) == p

# =========================
#  UTILIDADES
# =========================
def procesar_documento(ruta_pdf: str) -> str:
    os.makedirs(RESULTADO_DIR, exist_ok=True)
    name = Path(ruta_pdf).stem
    md_path = os.path.join(RESULTADO_DIR, f"{name}_completo.md")

    stqdm.write("Procesando con MarkItDown…")
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
    return sorted([f for f in os.listdir(RESULTADO_DIR) if f.endswith("_completo.md")], reverse=True) if os.path.isdir(RESULTADO_DIR) else []

def chat_sobre_md():
    st.header("Chat con el documento")
    contenido = st.session_state.contenido_doc

    if "history" not in st.session_state: st.session_state.history = []

    for m in st.session_state.history:
        st.chat_message("assistant" if m["role"]=="assistant" else "user").markdown(m["content"])

    quick = ["¿Cuál es el objetivo principal?", "¿Qué organismos participan?", "Fechas importantes", "Normativas mencionadas"]
    cols = st.columns(len(quick))
    for i,q in enumerate(quick):
        if cols[i].button(q, key=f"q{i}"):
            st.session_state.history.append({"role":"user","content":q})
            ans = chat_engine.chat(f"Contexto:\n{contenido}\n\nPregunta: {q}")
            st.session_state.history.append({"role":"assistant","content":ans})
            st.rerun()

    user_q = st.chat_input("Escribe tu pregunta…")
    if user_q:
        st.session_state.history.append({"role":"user","content":user_q})
        ans = chat_engine.chat(f"Contexto:\n{contenido}\n\nPregunta: {user_q}")
        st.session_state.history.append({"role":"assistant","content":ans})
        st.rerun()

# =========================
#  INTERFAZ STREAMLIT MAIN
# =========================
def main():
    # Login
    if not st.session_state.get("logged"):
        st.markdown("""<style>.login-box{border:2px solid #888;background:#2c2c2c;padding:2rem;border-radius:10px;max-width:400px;margin:4rem auto;color:#ddd}.login-title{text-align:center;font-size:1.8rem;font-weight:bold;margin-bottom:1.5rem}</style>""",unsafe_allow_html=True)
        st.markdown('<div class="login-box"><div class="login-title">Sistema OCR - Asistente</div>', unsafe_allow_html=True)
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión") and check_login(u,p):
            st.session_state.logged=True; st.session_state.user=u; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True); return

    # Sidebar
    st.sidebar.title(f"Bienvenido, {st.session_state.user}")
    if st.sidebar.button("Cerrar Sesión"): st.session_state.clear(); st.rerun()

    st.title("SISTEMA INTEGRADO OCR + CHAT")

    # Subir PDFs
    st.header("1. Subir y procesar PDFs")
    uploads = st.file_uploader("Sube uno o más PDFs", type="pdf", accept_multiple_files=True)
    if uploads:
        os.makedirs(PDF_DIR, exist_ok=True)
        for up in uploads:
            path = os.path.join(PDF_DIR, up.name)
            with open(path,"wb") as f: f.write(up.getbuffer())
            stqdm.write(f"Procesando {up.name}…")
            procesar_documento(path)

    # Sidebar lista
    st.sidebar.markdown("### Documentos Procesados")
    for md in list_markdowns():
        c1,c2 = st.sidebar.columns([0.85,0.15])
        if c1.button(f" {md}", key=f"sel_{md}"): st.session_state.sel=md
        if c2.button("✕", key=f"del_{md}"):
            os.remove(os.path.join(RESULTADO_DIR, md))
            st.rerun()

    # Chat
    if md := st.session_state.get("sel"):
        if "contenido_doc" not in st.session_state or st.session_state.get("contenido_doc_path") != md:
            with open(os.path.join(RESULTADO_DIR, md), "r", encoding="utf-8") as f:
                st.session_state.contenido_doc = f.read()
                st.session_state.contenido_doc_path = md
        chat_sobre_md()
    else:
        st.info("Selecciona un documento procesado desde la barra lateral.")

if __name__ == "__main__":
    main()