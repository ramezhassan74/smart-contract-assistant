from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import GOOGLE_API_KEY, LLM_MODEL
from app.retriever import get_retriever


SMART_CONTRACT_PROMPT = ChatPromptTemplate.from_template(
    """You are an expert Smart Contract Assistant specializing in
Solidity, Ethereum, and blockchain development.

Use the following context from the knowledge base to answer the question.
If the answer is not found in the context, say so clearly and provide
your general knowledge on the topic.

Always provide code examples when relevant and highlight security
considerations.

Context:
{context}

Question: {question}

Answer:"""
)


def _format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


def get_qa_chain():
    """Build a RAG chain using LCEL (LangChain Expression Language)."""
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Please set it in a .env file or as an environment variable."
        )

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
    )

    retriever = get_retriever()

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | SMART_CONTRACT_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask(question: str) -> dict:
    """Ask a question and return the answer with source documents."""
    chain, retriever = get_qa_chain()

    answer = chain.invoke(question)

    source_docs = retriever.invoke(question)

    sources = []
    for doc in source_docs:
        source_info = {
            "content": doc.page_content[:200] + "...",
            "metadata": doc.metadata,
        }
        sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources,
    }
