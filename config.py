"""
=========================================================
Saad Python Project
Configuration File
Version : 4.6
Author  : Saadullah Mir
=========================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PROJECT_NAME = "10 AI Together"
VERSION = "4.7"

APP_TITLE = "Usman Zafar AI Orchestrator"
PAGE_ICON = "🤖"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Set environment variables for LiteLLM
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY
os.environ["GROK_API_KEY"] = GROK_API_KEY
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

DEFAULT_THEME = "light"
DEFAULT_MODEL = "groq/llama-3.1-8b-instant"
MAX_PROMPT_LENGTH = 10000

# Display names for the sidebar - CLEAN PROFESSIONAL NAMES
AVAILABLE_MODELS = [
    "Groq Llama 3.1",
    "Mistral Small",
    "OpenRouter Pro",
    "NVIDIA Nemotron",
    "Groq Llama 3.1",
    "Mistral Small",
    "OpenRouter Pro",
    "NVIDIA Nemotron",
    "Groq Llama 3.1",
    "Mistral Small",
]

# ACTUAL MODEL IDs - ONLY CONFIRMED WORKING MODELS (with duplicates for 10)
RESPONDENT_MODELS = [
    # ---------- PRIMARY WORKING MODELS ----------
    "groq/llama-3.1-8b-instant",                              # 1. Groq ✓
    "mistral/mistral-small-latest",                           # 2. Mistral ✓
    "openrouter/openrouter/free",                             # 3. OpenRouter Pro ✓
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free",      # 4. NVIDIA Nemotron ✓
    
    # ---------- DUPLICATES FOR 10 MODELS ----------
    "groq/llama-3.1-8b-instant",                              # 5. Groq (duplicate)
    "mistral/mistral-small-latest",                           # 6. Mistral (duplicate)
    "openrouter/openrouter/free",                             # 7. OpenRouter (duplicate)
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free",      # 8. Nemotron (duplicate)
    "groq/llama-3.1-8b-instant",                              # 9. Groq (duplicate)
    "mistral/mistral-small-latest",                           # 10. Mistral (duplicate)
]

DATA_FOLDER = BASE_DIR / "data"
LOG_FOLDER = BASE_DIR / "logs"
EXPORT_FOLDER = BASE_DIR / "exports"

for folder in (DATA_FOLDER, LOG_FOLDER, EXPORT_FOLDER):
    folder.mkdir(exist_ok=True)

LOG_LEVEL = "INFO"
LOG_FILE = LOG_FOLDER / "app.log"
