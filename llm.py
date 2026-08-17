from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_MODEL

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0
)