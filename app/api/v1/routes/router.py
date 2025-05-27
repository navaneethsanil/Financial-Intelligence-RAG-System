from fastapi import APIRouter, File, UploadFile
from app.schemas import download_data_schema, document_upload_schema
from app.services import download_data_service
from app.services.document_upload_service import upload_document

router = APIRouter()


@router.post(
    "/download-data",
    response_model=download_data_schema.DownloadDataResponse,
    summary="Fetch and store data for given symbols",
    description="Accepts a list of symbols and triggers data fetching and storage operation.",
)
def download_data(request: download_data_schema.DownloadDataRequest):
    """
    Endpoint to fetch financial data for provided symbols and store it.

    Args:
        request (DownloadDataRequest): List of symbols to fetch data for.

    Returns:
        DownloadDataResponse: Message indicating success or failure.
    """
    return download_data_service.get_data(request)


@router.post(
    "/upload_document",
    response_model=document_upload_schema.DocumentUploadResponse,
    summary="Upload a document to be processed and stored",
    description="Accepts a file upload (.txt or .pdf) and processes it into the vector store.",
)
def upload_document_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to upload a document file for ingestion.

    Args:
        file (UploadFile): File uploaded by the client.

    Returns:
        DocumentUploadResponse: Message indicating the upload status.
    """
    return upload_document(file=file)
