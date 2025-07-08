import os
from dotenv import load_dotenv
from infrastructure.llm.openai_chat import OpenAIChat

# Cargar variables de entorno
load_dotenv()

# Configuración de Tesseract
CUSTOM_CONFIG = os.getenv("TESSERACT_CONFIG", r"--oem 3 --psm 6")

# Directorios
PDF_DIR = "data/pdfs"
RESULTADO_DIR = "data/resultado"

# API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicialización del motor de chat
CHAT_ENGINE = OpenAIChat(api_key=OPENAI_API_KEY)