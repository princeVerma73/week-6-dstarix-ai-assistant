import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = "gemini-3.6-flash"
EMBEDDING_MODEL = "gemini-embedding-2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5

API_KEY = os.getenv("API_KEY")