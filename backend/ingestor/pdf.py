"""PDF ingestor: loads and parses PDF files into text chunks for indexing."""
from langchain_community.document_loaders import PyPDFLoader

async def ingest_pdf(file_path: str):
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()
    print("documents pdf", documents)