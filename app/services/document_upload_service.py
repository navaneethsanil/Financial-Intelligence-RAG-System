import os
from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader, PDFMinerLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db.pinecone_db import init_pinecone
from app.schemas import document_upload_schema
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)

# Initialize Pinecone vector store and OpenAI embeddings
vector_store = init_pinecone()
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
index_name = os.getenv("INDEX_NAME")


def upload_document(file: UploadFile) -> dict:
    """
    Handles the upload, parsing, chunking, embedding, and storage of a document into a Pinecone vector store.

    Args:
        file (UploadFile): The file uploaded by the client (supports .txt and .pdf formats).

    Returns:
        dict: A response message indicating the outcome of the upload process.
    """
    # Define the directory and create it if it doesn't exist
    dir_path = "data/sample_docs"
    os.makedirs(dir_path, exist_ok=True)

    # Define the path where the uploaded file will be saved
    file_path = f"data/sample_docs/{file.filename}"

    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Choose the appropriate loader based on file extension
    if file.filename.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
    elif file.filename.endswith(".pdf"):
        loader = PDFMinerLoader(file_path)
    else:
        return {"message": "Unsupported file type"}

    # Load documents using the selected loader
    documents = loader.load()

    # Split documents into smaller chunks for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    # Add the document chunks to the Pinecone vector store
    vector_store.add_documents(documents=docs, index_name=index_name)

    return {"message": "Document uploaded to Pinecone successfully"}
