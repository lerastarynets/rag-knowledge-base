"""DOCX ingestor: loads and parses Word documents into text chunks for indexing."""
from langchain_community.document_loaders import Docx2txtLoader
from ingestor.pipeline import ingest_documents

async def ingest_docx(file_path: str, file_name: str):
    loader = Docx2txtLoader(file_path=file_path)
    documents = loader.load()
    print("ingesting docx")
    await ingest_documents(documents, file_name)
    print("docx ingested")