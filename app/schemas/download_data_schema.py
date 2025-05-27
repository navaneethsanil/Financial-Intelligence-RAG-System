from pydantic import BaseModel
from typing import List


class DownloadDataRequest(BaseModel):
    """
    Request model for initiating a data download operation.

    Attributes:
        symbols (List[str]):
            A list of string identifiers (e.g., stock tickers or asset codes)
            representing the data sources to be downloaded.
    """

    symbols: List[str]


class DownloadDataResponse(BaseModel):
    """
    Response model for a data download operation.

    Attributes:
        message (str):
            A human-readable message indicating the result or status
            of the download operation (e.g., "Download completed successfully").
    """

    message: str
