GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "gemini-embedding-2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 5

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")