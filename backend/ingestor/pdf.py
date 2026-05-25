"""PDF ingestor: loads and parses PDF files into text chunks for indexing."""
from langchain_community.document_loaders import PyPDFLoader
from ingestor.pipeline import ingest_documents

async def ingest_pdf(file_path: str):
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()
    print("ingesting pdf")
    await ingest_documents(documents)
    print("pdf ingested")