from fastapi import FastAPI
from app.api.v1.routes.router import router

# Initialize the FastAPI application instance
app = FastAPI(
    title="Financial Intelligence RAG System",
    description="An API for document ingestion, vector storage, and financial data analytics using RAG architecture.",
    version="1.0.0",
)

# API versioning prefix
prefix = "/api/v1"

# Include the versioned API router
app.include_router(router, prefix=prefix)
