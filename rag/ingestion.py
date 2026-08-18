from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

load_dotenv()


def ingest_document(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local("rag/vectorstore")

    return chunks


if __name__ == "__main__":

    chunks = ingest_document(
        "documents/sample.pdf"
    )

    print(f"Number of chunks: {len(chunks)}")
    print("FAISS vector store created successfully!")