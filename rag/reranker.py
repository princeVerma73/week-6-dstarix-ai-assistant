from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from pathlib import Path
import sys
import re

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


def rerank_documents(
    question,
    documents,
    top_k=3
):

    if not documents:
        return []

    documents_text = ""

    for i, document in enumerate(
        documents,
        start=1
    ):

        documents_text += f"""
DOCUMENT {i}:

{document.page_content}

"""

    prompt = f"""
You are a document relevance evaluator.

User question:
{question}

Below are multiple retrieved documents.

{documents_text}

Task:
Give a relevance score from 0 to 10 for EACH document.

10 = highly relevant
0 = completely irrelevant

Return ONLY the scores in this exact format:

Document 1: 8
Document 2: 5
Document 3: 10
Document 4: 2
Document 5: 7

Do not provide explanations.
Do not return any other text.
"""

    try:

        response = llm.invoke(prompt)

        result = extract_text(
            response.content
        )

        print("\nReranker response:")
        print(result)

        scores = {}

        for match in re.finditer(
            r"Document\s+(\d+)\s*:\s*(\d+(?:\.\d+)?)",
            result,
            re.IGNORECASE
        ):

            document_number = int(
                match.group(1)
            )

            score = float(
                match.group(2)
            )

            scores[
                document_number
            ] = score

        scored_documents = []

        for i, document in enumerate(
            documents,
            start=1
        ):

            score = scores.get(
                i,
                0
            )

            scored_documents.append(
                (
                    score,
                    i,
                    document
                )
            )

        scored_documents.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            document
            for score, index, document
            in scored_documents[:top_k]
        ]

    except Exception as e:

        print(
            f"Reranking failed: {e}"
        )

        return documents[:top_k]


if __name__ == "__main__":

    from retrieval import (
        retrieve_documents
    )

    from query_transform import (
        transform_query
    )

    question = (
        "What happens in the second phase?"
    )

    search_query = transform_query(
        question
    )

    print(
        "Transformed query:"
    )

    print(search_query)

    documents = retrieve_documents(
        search_query,
        k=5
    )

    print(
        f"\nRetrieved {len(documents)} documents."
    )

    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=3
    )

    print(
        f"Reranked to "
        f"{len(reranked_documents)} documents."
    )

    print(
        "\nReranked Documents:\n"
    )

    for i, document in enumerate(
        reranked_documents,
        start=1
    ):

        print(
            f"--- Document {i} ---"
        )

        print(
            document.page_content[:500]
        )

        print(
            "\nMetadata:"
        )

        print(
            document.metadata
        )

        print()