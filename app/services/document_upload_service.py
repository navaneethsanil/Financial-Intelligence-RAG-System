import os
from fastapi import UploadFile
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv(override=True)

# Initialize Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Path to store FAISS index
faiss_index_path = "vectorstore/faiss_index"


def upload_document(file: UploadFile) -> dict:
    """
    Handles the upload, parsing, chunking, embedding, and storage of a document into a FAISS vector store.

    Args:
        file (UploadFile): The file uploaded by the client (supports .txt and .pdf formats).

    Returns:
        dict: A response message indicating the outcome of the upload process.
    """
    # Ensure directories exist
    dir_path = "data/sample_docs"
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs("vectorstore", exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(dir_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Choose the appropriate loader
    if file.filename.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
    elif file.filename.endswith(".pdf"):
        loader = PDFMinerLoader(file_path)
    else:
        return {"message": "Unsupported file type"}

    # Load and split the document
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    # Load existing FAISS index or create a new one
    if os.path.exists(faiss_index_path):
        faiss_store = FAISS.load_local(
            faiss_index_path, embeddings, allow_dangerous_deserialization=True
        )
        faiss_store.add_documents(docs)
    else:
        faiss_store = FAISS.from_documents(docs, embeddings)

    # Save the updated FAISS index
    faiss_store.save_local(faiss_index_path)

    return {"message": "Document uploaded and indexed with FAISS successfully"}
