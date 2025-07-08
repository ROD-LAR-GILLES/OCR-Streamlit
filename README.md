# OCR-Streamlit: Sistema Integrado de OCR y Chat

Este proyecto es una aplicación basada en Streamlit que combina un sistema de reconocimiento óptico de caracteres (OCR) con un asistente de chat impulsado por modelos de lenguaje de OpenAI. Permite procesar documentos PDF, extraer texto y tablas, y realizar consultas sobre el contenido procesado.

## 🚀 Características

- **OCR avanzado**: Utiliza PyMuPDF, Tesseract y pdfplumber para extraer texto y tablas de documentos PDF
- **Procesamiento de tablas**: Extrae tablas utilizando Camelot y pdfplumber
- **Chat contextual**: Realiza preguntas sobre el contenido de los documentos procesados utilizando modelos de lenguaje de OpenAI
- **Interfaz intuitiva**: Una interfaz interactiva basada en Streamlit para subir, procesar y consultar documentos
- **Autenticación**: Sistema de login para controlar el acceso a la aplicación
- **Soporte multiidioma**: OCR optimizado para español

## 📋 Prerrequisitos

- Docker y Docker Compose instalados en tu sistema
- Clave API de OpenAI

## ⚡ Inicio Rápido con Docker

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd OCR-Streamlit
```

### 2. Configurar variables de entorno
Copia el archivo de ejemplo y configura tu clave API:
```bash
cp .env.example .env
```

Edita el archivo `.env` y añade tu clave API de OpenAI:
```bash
OPENAI_API_KEY=tu_clave_api_aqui
```

### 3. Ejecutar con Docker Compose
```bash
docker-compose up --build
```

### 4. Acceder a la aplicación
Abre tu navegador y ve a: http://localhost:8501

## 🔐 Credenciales de Acceso

La aplicación incluye un sistema de autenticación. Puedes usar las siguientes credenciales predeterminadas:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin   | password   | Administrador |
| user    | passuser   | Usuario estándar |
| guest   | guestpass  | Invitado |

## 📁 Estructura del Proyecto

```
.
├── adapters/
│   ├── embedding/
│   │   └── embedding_openai.py      # Embeddings para búsqueda semántica
│   ├── ocr/
│   └── pdf/
├── application/
│   ├── chat_retrieval.py            # Lógica de búsqueda y recuperación
│   ├── procesar_md.py               # Procesamiento de documentos Markdown
│   ├── use_cases.py                 # Casos de uso principales
│   └── services/
│       ├── auth.py                  # Servicio de autenticación
│       └── pdf_processor.py         # Procesador principal de PDFs
├── data/
│   ├── pdfs/                        # Almacenamiento de PDFs subidos
│   └── resultado/                   # Documentos procesados (Markdown)
├── domain/
│   └── document_chunk.py            # Modelo de chunks de documentos
├── infrastructure/
│   ├── config/
│   │   └── config.py                # Configuración global
│   ├── llm/
│   │   └── openai_chat.py           # Cliente de OpenAI
│   └── markdown/
│       └── markdown_converter.py
├── interfaces/
│   └── streamlit/
│       └── streamlit_app.py         # Interfaz principal de Streamlit
├── .env                             # Variables de entorno (configurar)
├── .env.example                     # Ejemplo de variables de entorno
├── docker-compose.yml               # Configuración de Docker Compose
├── dockerfile                       # Imagen Docker
└── requirements.txt                 # Dependencias Python
```

## 🐳 Comandos Docker Útiles

### Ejecutar en segundo plano
```bash
docker-compose up -d
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Detener la aplicación
```bash
docker-compose down
```

### Reconstruir la imagen (después de cambios)
```bash
docker-compose up --build
```

### Ejecutar solo el build
```bash
docker-compose build
```

## 🔧 Desarrollo Local (sin Docker)

Si prefieres ejecutar la aplicación localmente sin Docker:

### 1. Instalar dependencias del sistema
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-spa

# macOS (con Homebrew)
brew install poppler tesseract tesseract-lang
```

### 2. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
streamlit run interfaces/streamlit/streamlit_app.py
```

## 📖 Uso de la Aplicación

### 1. Iniciar Sesión
- Accede a la aplicación y usa las credenciales proporcionadas
- El sistema te llevará al dashboard principal

### 2. Procesar Documentos PDF
- Ve a la pestaña "📤 Procesar Documentos"
- Sube uno o más archivos PDF
- La aplicación extraerá automáticamente texto y tablas

### 3. Chat con Documentos
- Ve a la pestaña "💬 Chat con Documentos"
- Selecciona un documento procesado desde la barra lateral
- Usa las preguntas rápidas generadas automáticamente
- O escribe tus propias preguntas sobre el documento

### 4. Gestión de Documentos
- En la barra lateral puedes ver todos los documentos procesados
- Selecciona documentos para hacer consultas
- Elimina documentos que ya no necesites

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit
- **OCR**: PyMuPDF, Tesseract, pdfplumber
- **Extracción de Tablas**: Camelot, pdfplumber
- **IA/Chat**: OpenAI GPT-4
- **Embeddings**: OpenAI text-embedding-3-small
- **Containerización**: Docker & Docker Compose
- **Conversión**: MarkItDown

## 🔍 Funcionalidades Avanzadas

- **OCR Inteligente**: Detecta automáticamente si un PDF necesita OCR
- **Extracción de Tablas**: Combina múltiples herramientas para mejor precisión
- **Chat Contextual**: Respuestas basadas únicamente en el contenido del documento
- **Preguntas Rápidas**: Generación automática de preguntas relevantes
- **Gestión de Sesiones**: Sistema de autenticación integrado

## 🚨 Solución de Problemas

### Error de permisos con Docker
```bash
sudo docker-compose up --build
```

### La aplicación no carga
- Verifica que el puerto 8501 esté libre
- Revisa los logs: `docker-compose logs`

### Error de API de OpenAI
- Verifica que tu clave API sea válida
- Asegúrate de tener créditos en tu cuenta de OpenAI

### Problemas con OCR
- Los documentos deben ser PDFs válidos
- Para mejor precisión, usa PDFs con buena calidad de imagen

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

---

⚡ **¡Listo para procesar tus documentos con IA!** 🚀

