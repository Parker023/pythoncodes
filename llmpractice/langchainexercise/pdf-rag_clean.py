
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.prompts import PromptTemplate, ChatPromptTemplate

import ollama
import os
import logging

DOC_PATH = "../data/BOI.pdf"

MODEL = "llama3.1"

EMBEDDING_MODEL = "nomic-embed-text"

RAG_COLLECTION_NAME = "simple-rag"

logging.basicConfig(level=logging.INFO)


def ingest_pdf(docpath):
    """Load PDF documents."""
    if os.path.exists(docpath):
        loader = UnstructuredLoader(file_path=docpath)
        data = loader.load()
        logging.info("PDF loaded successfully.")
        return data
    else:
        logging.error("PDF not found.")
        return None


def split_documents(documents):
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(documents=documents)

    logging.info("Documents split into chunks.")
    return chunks


def create_vector_database(chunks):
    """Create a vector database from document chunks."""
    # Pull the embedding model if not already available
    ollama.pull(EMBEDDING_MODEL)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag"
    )
    logging.info("Vector database created.")
    return vector_db


def cleanup_metadata(chunks):
    """Clean up metadata for each chunk."""
    for chunk in chunks:
        chunk.metadata = {
            "page_number": chunk.metadata.get("page_number"),
            "category": chunk.metadata.get("category"),
        }


def create_retriever(vector_db, llm):
    """Create a multi-query retriever."""
    query_prompt = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
            different versions of the given user question to retrieve relevant documents from
            a vector database. By generating multiple perspectives on the user question, your
            goal is to help the user overcome some of the limitations of the distance-based
            similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        retriever=vector_db.as_retriever(),
        llm=llm,
        prompt=query_prompt,
    )
    logging.info("Retriever created.")
    return retriever


def create_chain(retriever, llm):
    """Create a chain for answering questions."""
    # RAG prompt

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {
                "context": retriever, "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
    )
    logging.info("Chain created.")
    return chain


def main():
    # Load and process the PDF document
    data = ingest_pdf(DOC_PATH)

    # Split the documents into chunks
    chunks = split_documents(data)

    # clean up the metadata
    cleanup_metadata(chunks)

    # Create the vector database
    vector_db = create_vector_database(chunks)

    # Create the retriever
    llm = ChatOllama(model=MODEL)
    retriever = create_retriever(vector_db, llm)

    # Create the chain
    chain = create_chain(retriever, llm)

    # Example query
    question = "How to report BOI?"

    # Get the response
    res = chain.invoke(input=question)
    print("Response:")
    print(res)


if __name__ == "__main__":
    main()
