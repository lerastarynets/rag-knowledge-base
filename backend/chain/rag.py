"""RAG chain: orchestrates retrieval and generation to produce grounded answers."""

from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableSerializable
from retriever import search, assert_relevance
from .prompts import RAG_PROMPT
from operator import itemgetter
from services import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

def _format_context(context: list[Document]) -> str:
    parts = []
    for doc in context or []:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        citation = f"[{source}, page {page}]" if page is not None else f"[{source}]"
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