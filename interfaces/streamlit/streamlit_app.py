#!/usr/bin/env python
"""
Sistema OCR + Chat - Interfaz Streamlit

Aplicación web para procesar documentos PDF con OCR y chat asistido por IA.
"""

import os
from pathlib import Path
from typing import List, Optional

import streamlit as st
from stqdm import stqdm
from dotenv import load_dotenv

# Importaciones de configuración y servicios
from infrastructure.config.config import PDF_DIR, RESULTADO_DIR, CHAT_ENGINE
from application.services.pdf_processor import PDFProcessor
from application.services.auth import check_login

# =========================
#  CONFIGURACIÓN Y CONSTANTES
# =========================

# Cargar variables de entorno
load_dotenv()

# Configuración de página Streamlit
st.set_page_config(
    page_title="Sistema OCR + Chat",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Instancias globales


@st.cache_resource
def get_pdf_processor():
    """Crear instancia de PDFProcessor (cached)."""
    return PDFProcessor()


@st.cache_resource
def get_chat_engine():
    """Obtener motor de chat (cached)."""
    return CHAT_ENGINE


# Inicializar servicios
pdf_processor = get_pdf_processor()
chat_engine = get_chat_engine()

# =========================
#  FUNCIONES DE UTILIDAD
# =========================


def ensure_directories() -> None:
    """Crear directorios necesarios si no existen."""
    for directory in [PDF_DIR, RESULTADO_DIR]:
        os.makedirs(directory, exist_ok=True)


def get_processed_documents() -> List[str]:
    """Obtener lista de documentos procesados."""
    if not os.path.isdir(RESULTADO_DIR):
        return []

    files = [
        f for f in os.listdir(RESULTADO_DIR)
        if f.endswith("_completo.md")
    ]
    return sorted(files, reverse=True)


@st.cache_data
def load_document_content(md_file: str) -> str:
    """Cargar contenido de documento (cached)."""
    md_path = os.path.join(RESULTADO_DIR, md_file)
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Archivo no encontrado: {md_file}")
        return ""


def process_uploaded_file(uploaded_file) -> Optional[str]:
    """Procesar archivo PDF subido."""
    ensure_directories()

    file_path = os.path.join(PDF_DIR, uploaded_file.name)

    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Procesar documento
    with st.spinner(f"Procesando {uploaded_file.name}..."):
        return pdf_processor.procesar_documento(file_path)

# =========================
#  COMPONENTES DE INTERFAZ
# =========================


def render_login_form() -> None:
    """Renderizar un formulario de login usando únicamente componentes nativos de Streamlit."""

    # Título centrado
    st.markdown("<h1 style='text-align: center;'>🔐 Bienvenido al Sistema OCR + Chat</h1>",
                unsafe_allow_html=True)

    # Espaciado visual entre título y formulario
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    # Centramos el formulario usando columnas
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        with st.container(border=True):
            st.subheader("Iniciar sesión", divider="rainbow")

            username = st.text_input(
                "Usuario",
                placeholder="Ingresa tu nombre de usuario",
                label_visibility="visible",
            )
            password = st.text_input(
                "Contraseña",
                placeholder="Ingresa tu contraseña",
                type="password",
                label_visibility="visible",
            )
            login_clicked = st.button(
                "✨  Iniciar Sesión", use_container_width=True)

            if login_clicked:
                if check_login(username, password):
                    st.success("✔️  Sesión iniciada correctamente", icon="✅")
                    st.session_state.logged = True
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("❌  Credenciales inválidas")

    # Footer centrado
    st.markdown(
        "<p style='text-align:center; font-size:0.75rem; color:gray'>&copy; 2025 • Sistema OCR + Chat</p>",
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Renderizar barra lateral con diseño profesional y limpio."""
    st.sidebar.markdown("### Bienvenido, **{}**".format(st.session_state.user))
    
    # Botón de cerrar sesión en la parte superior
    if st.sidebar.button("Cerrar Sesión", use_container_width=True, type="primary", key="logout_btn_top"):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")

    # Sección de documentos
    st.sidebar.markdown("#### Documentos Procesados")
    documents = get_processed_documents()

    if not documents:
        st.sidebar.info("No hay documentos procesados.")
    else:
        for doc in documents:
            doc_name = doc.replace("_completo.md", "")
            col1, col2 = st.sidebar.columns([0.85, 0.15])
            
            # Botón para seleccionar
            if col1.button(f"📄 {doc_name}", key=f"sel_{doc}", use_container_width=True):
                st.session_state.selected_document = doc
                st.cache_data.clear()
            
            # Botón para eliminar
            if col2.button("🗑️", key=f"del_{doc}", help=f"Eliminar {doc_name}"):
                try:
                    os.remove(os.path.join(RESULTADO_DIR, doc))
                    st.sidebar.success(f"Eliminado: {doc_name}")
                    st.rerun()
                except FileNotFoundError:
                    st.sidebar.error("Archivo no encontrado")

    st.sidebar.markdown("---")
    
    # Información del sistema
    st.sidebar.markdown("#### ℹ️ Sistema")
    st.sidebar.caption("OCR + Chat v1.0")
    st.sidebar.caption("Desarrollado con Streamlit")


def render_file_upload() -> None:
    """Renderizar sección de carga de archivos."""
    st.header("Subir y Procesar PDFs")

    uploaded_files = st.file_uploader(
        "Selecciona uno o más archivos PDF",
        type=["pdf"],
        accept_multiple_files=True,
        help="Puedes subir múltiples archivos PDF a la vez"
    )

    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, uploaded_file in enumerate(uploaded_files):
            progress = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Procesando {uploaded_file.name}...")

            result = process_uploaded_file(uploaded_file)
            if result:
                st.success(f"✅ {uploaded_file.name} procesado exitosamente")
            else:
                st.error(f"❌ Error procesando {uploaded_file.name}")

        status_text.text("¡Procesamiento completo!")
        st.balloons()


def generate_quick_questions(content: str) -> List[str]:
    """Generar preguntas rápidas basadas en el contenido."""
    try:
        prompt = f"""Analiza el siguiente contenido de documento y genera exactamente 4 preguntas relevantes y específicas.
        Las preguntas deben ser claras, concisas y estar relacionadas con el contenido del documento.
        
        Formato de respuesta: una pregunta por línea, sin numeración.
        
        Contenido del documento:
        {content[:2000]}...
        """

        response = chat_engine.chat(prompt)
        questions = [q.strip() for q in response.split('\n') if q.strip(
        ) and not q.strip().startswith(('1.', '2.', '3.', '4.'))]
        return questions[:4]  # Limitar a 4 preguntas
    except Exception as e:
        st.error(f"Error generando preguntas: {e}")
        return [
            "¿Cuál es el tema principal del documento?",
            "¿Qué puntos importantes se mencionan?",
            "¿Hay datos o estadísticas relevantes?",
            "¿Cuáles son las conclusiones principales?"
        ]


def render_chat_interface() -> None:
    """Renderizar interfaz de chat."""
    selected_doc = st.session_state.get("selected_document")
    if not selected_doc:
        st.info(
            "📋 Selecciona un documento desde la barra lateral para comenzar el chat")
        return

    st.header(f" Chat con: {selected_doc.replace('_completo.md', '')}")

    # Cargar contenido del documento
    content = load_document_content(selected_doc)
    if not content:
        return

    # Inicializar historial de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generar preguntas rápidas
    if "quick_questions" not in st.session_state or st.session_state.get("current_doc") != selected_doc:
        with st.spinner("Generando preguntas rápidas..."):
            st.session_state.quick_questions = generate_quick_questions(
                content)
            st.session_state.current_doc = selected_doc

    # Mostrar preguntas rápidas
    st.subheader("Preguntas Rápidas")
    cols = st.columns(2)

    for i, question in enumerate(st.session_state.quick_questions):
        col_idx = i % 2
        if cols[col_idx].button(f"❓ {question}", key=f"quick_q_{i}", use_container_width=True):
            handle_user_question(question, content)

    # Input de chat
    user_question = st.chat_input("Escribe tu pregunta sobre el documento...")
    if user_question:
        handle_user_question(user_question, content)


def handle_user_question(question: str, content: str) -> None:
    """Manejar pregunta del usuario."""
    # Añadir pregunta del usuario al historial
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.markdown(question)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            prompt = f"""Contexto del documento:
{content}

Pregunta del usuario: {question}

Por favor, responde de manera clara y precisa basándote únicamente en el contenido del documento proporcionado."""

            try:
                response = chat_engine.chat(prompt)
                st.markdown(response)

                # Añadir respuesta al historial
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ Error al generar respuesta: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": error_msg})

    st.rerun()

# =========================
#  FUNCIÓN PRINCIPAL
# =========================


def main() -> None:
    """Función principal de la aplicación."""
    # Verificar autenticación
    if not st.session_state.get("logged"):
        render_login_form()
        return

    # Renderizar interfaz principal
    render_sidebar()

    # Título principal
    st.title("Sistema Integrado OCR + Chat")
    st.markdown("---")

    # Tabs principales
    tab1, tab2 = st.tabs(["📤 Procesar Documentos", "💬 Chat con Documentos"])

    with tab1:
        render_file_upload()

    with tab2:
        render_chat_interface()


if __name__ == "__main__":
    main()
