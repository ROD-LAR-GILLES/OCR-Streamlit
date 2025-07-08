OCR-Streamlit: Sistema Integrado de OCR y Chat

Este proyecto es una aplicación basada en Streamlit que combina un sistema de reconocimiento óptico de caracteres (OCR) con un asistente de chat impulsado por modelos de lenguaje de OpenAI. Permite procesar documentos PDF, extraer texto y tablas, y realizar consultas sobre el contenido procesado.

Características
	•	OCR avanzado: Utiliza PyMuPDF, Tesseract y pdfplumber para extraer texto y tablas de documentos PDF.
	•	Procesamiento de tablas: Extrae tablas utilizando Camelot y pdfplumber.
	•	Chat contextual: Realiza preguntas sobre el contenido de los documentos procesados utilizando modelos de lenguaje de OpenAI.
	•	Interfaz intuitiva: Una interfaz interactiva basada en Streamlit para subir, procesar y consultar documentos.

Estructura del Proyecto

.
├── adapters/
│   ├── embedding/
│   │   └── embedding_openai.py
│   ├── ocr/
│   └── pdf/
├── application/
│   ├── chat_retrieval.py
│   ├── procesar_md.py
│   ├── use_cases.py
│   └── services/
│       ├── auth.py
│       └── pdf_processor.py
├── data/
│   ├── pdfs/
│   └── resultado/
├── domain/
│   ├── document_chunk.py
│   └── models.py
├── infrastructure/
│   ├── config/
│   │   └── config.py
│   ├── llm/
│   │   └── openai_chat.py
│   ├── markdown/
│   │   └── markdown_converter.py
├── interfaces/
│   └── streamlit/
│       └── streamlit_app.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── dockerfile
├── main.py
├── README.md
└── requirements.txt


⸻

✨ Optimizaciones Realizadas en el Sistema OCR + Chat

