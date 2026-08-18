from pathlib import Path
import sys

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from config import EMBEDDING_MODEL, TOP_K

load_dotenv()


def retrieve_documents(query, k=TOP_K):

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    vectorstore = FAISS.load_local(
        "rag/vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    documents = vectorstore.similarity_search(
        query,
        k=k
    )

    return documents


if __name__ == "__main__":

    question = "What happens in the second phase?"

    documents = retrieve_documents(
        question,
        k=3
    )

    print(
        f"Retrieved {len(documents)} documents."
    )

    for i, document in enumerate(
        documents,
        start=1
    ):

        print(f"\n--- Document {i} ---")

        print(
            document.page_content[:500]
        )

        print(
            "Metadata:",
            document.metadata
        )