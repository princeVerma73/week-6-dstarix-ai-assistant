from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from dotenv import load_dotenv

from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from config import GEMINI_MODEL

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0
)


def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:
                    parts.append(
                        str(item["text"])
                    )

        return "".join(parts).strip()

    return str(content)


def transform_query(question):

    prompt = f"""
You are a search query optimizer.

Rewrite the user's question into a concise search query
that will help retrieve the most relevant information
from a document knowledge base.

Do not answer the question.
Only return the improved search query.

User question:
{question}
"""

    response = llm.invoke(prompt)

    return extract_text(
        response.content
    ).strip()


if __name__ == "__main__":

    question = (
        "What happens in the second phase?"
    )

    transformed_query = transform_query(
        question
    )

    print("Original query:")
    print(question)

    print("\nTransformed query:")
    print(transformed_query)