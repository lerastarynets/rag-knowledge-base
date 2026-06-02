"""RAG chain: orchestrates retrieval and generation to produce grounded answers."""

from operator import itemgetter
from urllib.parse import urlparse

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableSerializable

from retriever import assert_relevance, search
from services import llm

from .prompts import RAG_PROMPT


def _format_citation(doc: Document) -> str:
    metadata = doc.metadata
    source_type = metadata.get("source_type")
    source = metadata.get("source", "unknown")

    if source_type in ("pdf", "docx"):
        page = metadata.get("page")
        return f"[{source}, page {page}]" if page is not None else f"[{source}]"

    if source_type == "url":
        title = metadata.get("title") or "Untitled"
        domain = urlparse(source).netloc or source
        return f"[Article: {domain} — {title}]"

    if source_type == "youtube":
        title = metadata.get("title", "Unknown")
        author = metadata.get("author", "Unknown")
        return f'[Video: "{title}" by {author}]'

    page = metadata.get("page")
    return f"[{source}, page {page}]" if page is not None else f"[{source}]"


def _format_context(context: list[Document]) -> str:
    parts = []
    for doc in context or []:
        citation = _format_citation(doc)
        parts.append(f"{citation}\n{doc.page_content.strip()}")
    return "\n\n".join(parts)

def rag_chain() -> RunnableSerializable:
    retrieval_chain= (
        RunnablePassthrough.assign(context=itemgetter("question") 
                                | RunnableLambda(search) | RunnableLambda(assert_relevance) | RunnableLambda(_format_context))
                                | RAG_PROMPT
                                | llm
                                | StrOutputParser()
                                )
    return retrieval_chain