# OCR-Streamlit: Sistema Integrado de OCR y Chat

Este proyecto es una aplicación basada en **Streamlit** que combina un sistema de reconocimiento óptico de caracteres (OCR) con un asistente de chat impulsado por modelos de lenguaje de OpenAI. Permite procesar documentos PDF, extraer texto y tablas, y realizar consultas sobre el contenido procesado.

## Características

- **OCR avanzado**: Utiliza PyMuPDF, Tesseract y pdfplumber para extraer texto y tablas de documentos PDF.
- **Procesamiento de tablas**: Extrae tablas utilizando Camelot y pdfplumber.
- **Chat contextual**: Realiza preguntas sobre el contenido de los documentos procesados utilizando modelos de lenguaje de OpenAI.
- **Interfaz intuitiva**: Una interfaz interactiva basada en Streamlit para subir, procesar y consultar documentos.

## Estructura del Proyecto

```plaintext
.
├── adapters/
│   ├── embedding/
│   │   └── [embedding_openai.py](http://_vscodecontentref_/0)
│   ├── ocr/
│   └── pdf/
├── application/
│   ├── [chat_retrieval.py](http://_vscodecontentref_/1)
│   ├── [procesar_md.py](http://_vscodecontentref_/2)
│   ├── [use_cases.py](http://_vscodecontentref_/3)
│   └── services/
│       ├── [auth.py](http://_vscodecontentref_/4)
│       └── [pdf_processor.py](http://_vscodecontentref_/5)
├── data/
│   ├── pdfs/
│   └── resultado/
├── domain/
│   ├── [document_chunk.py](http://_vscodecontentref_/6)
│   └── [models.py](http://_vscodecontentref_/7)
├── infrastructure/
│   ├── config/
│   │   └── [config.py](http://_vscodecontentref_/8)
│   ├── llm/
│   │   └── [openai_chat.py](http://_vscodecontentref_/9)
│   ├── markdown/
│   │   └── [markdown_converter.py](http://_vscodecontentref_/10)
├── interfaces/
│   └── streamlit/
│       └── [streamlit_app.py](http://_vscodecontentref_/11)
├── .env
├── [.env.example](http://_vscodecontentref_/12)
├── .gitignore
├── [docker-compose.yml](http://_vscodecontentref_/13)
├── dockerfile
├── [main.py](http://_vscodecontentref_/14)
├── [README.md](http://_vscodecontentref_/15)
└── [requirements.txt](http://_vscodecontentref_/16)