from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pathlib import Path
import sys
import re
# Allow imports from project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import GEMINI_MODEL

load_dotenv()

# Gemini model
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0
)

def rerank_documents(question, documents, top_k=3):
    if not documents:
        return []
    # Build all documents into one prompt
    documents_text = ""

    for i, document in enumerate(documents, start=1):
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
"""

    try:
        response = llm.invoke(prompt)

        result = response.content.strip()

        print("\nReranker response:")
        print(result)

        # Extract scores
        scores = {}

        for match in re.finditer(
            r"Document\s+(\d+)\s*:\s*(\d+(?:\.\d+)?)",
            result,
            re.IGNORECASE
        ):
            document_number = int(match.group(1))
            score = float(match.group(2))

            scores[document_number] = score

        scored_documents = []

        for i, document in enumerate(documents, start=1):

            score = scores.get(i, 0)

            scored_documents.append(
                (score, document)
            )

        # Highest score first
        scored_documents.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            document
            for score, document in scored_documents[:top_k]
        ]

    except Exception as e:

        print(f"Reranking failed: {e}")
        # Fallback:
        # If Gemini fails, return the original top documents
        return documents[:top_k]


# Test complete reranking pipeline
if __name__ == "__main__":
    from retrieval import retrieve_documents
    from query_transform import transform_query

    question = "What happens in the second phase?"

    # Step 1: Transform question
    search_query = transform_query(question)

    print("Transformed query:")
    print(search_query)

    # Step 2: Retrieve documents
    documents = retrieve_documents(
        search_query,
        k=5
    )

    print(f"\nRetrieved {len(documents)} documents.")

    # Step 3: Rerank
    reranked_documents = rerank_documents(
        question,
        documents,
        top_k=3
    )

    print(f"Reranked to {len(reranked_documents)} documents.")
    print("\nReranked Documents:\n")

    for i, document in enumerate(
        reranked_documents,
        start=1
    ):
        print(f"--- Document {i} ---")
        print(document.page_content[:500])
        print()