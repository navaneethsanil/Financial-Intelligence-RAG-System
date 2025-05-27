import os
from pinecone import ServerlessSpec, Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file (overrides existing variables)
load_dotenv(override=True)

# Fetch API keys and configuration from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI embeddings with a specific model and API key
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)


def init_pinecone() -> PineconeVectorStore:
    """
    Initialize and return a Pinecone vector store instance.

    This function:
    - Connects to Pinecone using the provided API key.
    - Checks if the specified index exists; creates it if not.
    - Configures the index with dimension and similarity metric.
    - Returns a PineconeVectorStore wrapped around the Pinecone index and OpenAI embeddings.

    Returns:
        PineconeVectorStore: A vector store instance ready for document indexing and querying.
    """
    pc = Pinecone(api_key=pinecone_api_key)

    # Create index if it does not exist
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,  # Dimension size for OpenAI embeddings
            metric="cosine",  # Similarity metric for vector search
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    # Connect to the index
    index = pc.Index(index_name)

    # Create the vector store using the index and embeddings
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    return vector_store
