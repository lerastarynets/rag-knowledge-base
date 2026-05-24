"""DOCX ingestor: loads and parses Word documents into text chunks for indexing."""
from langchain_community.document_loaders import Docx2txtLoader

async def ingest_docx(file_path: str):
    loader = Docx2txtLoader(file_path=file_path)
    documents = loader.load()
    print("documents docx", documents)