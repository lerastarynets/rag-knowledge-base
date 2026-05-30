"""RAG chain: orchestrates retrieval and generation to produce grounded answers."""

from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableSerializable
from retriever import search, assert_relevance
from .prompts import RAG_PROMPT
from operator import itemgetter
from services import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

def _format_context(context: list[Document]) -> str:
    return "\n".join([f"[{doc.metadata['source']}, page {doc.metadata['page']}]\n{doc.page_content}\n\n" for doc in context or []])

def rag_chain() -> RunnableSerializable:
    retrieval_chain= (
        RunnablePassthrough.assign(context=itemgetter("question") 
                                | RunnableLambda(search) | RunnableLambda(assert_relevance) | RunnableLambda(_format_context))
                                | RAG_PROMPT
                                | llm
                                | StrOutputParser()
                                )
    return retrieval_chain