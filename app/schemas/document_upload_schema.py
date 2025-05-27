from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    """
    Response model for document upload operations.

    Attributes:
        message (str): A descriptive message indicating the result of the upload operation.
    """

    message: str  # Message to convey the outcome of the document upload (e.g., "Upload successful")
