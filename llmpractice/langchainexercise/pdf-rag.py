## 1. Ingest PDF Files
# 2. Extract Text from PDF Files and split into small chunks
# 3. Send the chunks to embedding model
# 4. Save the embeddings to vector database
# 5. Perform similarity search on the vector database to find similar documents
# 6. Retrieve the similar documents and present them to the user
## run pip install -r requirements.txt to install the required packages


# from langchain_community.document_loaders import OnlinePDFLoader
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
import time

doc_path = "../data/BOI.pdf"

model = "llama3.1"

start_time = time.time()

# Load pdf file
if os.path.exists(doc_path):
    loader = UnstructuredLoader(file_path=doc_path)
    data = loader.load()
    print("Loaded document")
else:
    print("No document")

print(f"Time taken to load the document is {time.time() - start_time} seconds")
# first_page=data[0].page_content
# print(first_page)
#
# for doc in data[:10]:
#     print(doc.page_content)

# END of PDF ingestion

# 2. Extract Text from PDF Files and split into small chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(documents=data)

print(f"Number of chunks: {len(chunks)}")
print("Splitting completed.")
# print("Example chunk: ", chunks[0])


# END of text extraction

# Pull the embedding model
ollama.pull("nomic-embed-text")

print("Embedding model pulled.")
# 3. Send the chunks to the embedding model

# clean up the metadata
for chunk in chunks:
    chunk.metadata = {
        "page_number": chunk.metadata.get("page_number"),
        "category": chunk.metadata.get("category"),
    }

print("Metadata cleaned up.")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag"
)

print("Vector database created.")
# set up our model to use the vector database

llm = ChatOllama(model=model)

print("LLM Model set up.")

QUERY_PROMPT = PromptTemplate(
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
    prompt=QUERY_PROMPT,
)

print("Retriever set up.")
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

print("Chain set up.")

# res = chain.invoke(
#     input=("what are the main points as a business owner I should be aware of?",)
# )
# res=chain.invoke(input=("what is the document about?",))

res=chain.invoke("how to report BOI?")
print(res)
