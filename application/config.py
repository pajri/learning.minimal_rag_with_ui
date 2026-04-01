import os 
import sys 
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# constants
DISTANCE_THRESHOLD = 0.5
LANGUAGE_MODEL = "qwen2:0.5b"
EVALUATION_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# env variables
load_dotenv(dotenv_path=f'{BASE_DIR}/.env')

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")