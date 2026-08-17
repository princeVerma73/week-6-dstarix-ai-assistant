from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import EMBEDDING_MODEL, TOP_K
from rag.query_transform import transform_query

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

    # Transform the original question
    search_query = transform_query(question)

    print("Original query:")
    print(question)

    print("\nTransformed query:")
    print(search_query)

    # Retrieve using transformed query
    documents = retrieve_documents(
        search_query,
        k=3
    )

    print("\nRetrieved documents:\n")
    for i, document in enumerate(documents):

        print(f"--- Document {i + 1} ---")
        print(document.page_content[:500])
        print()