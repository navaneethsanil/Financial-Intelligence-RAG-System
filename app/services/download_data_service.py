from fastapi import HTTPException
from app.utils.store_data import fetch_and_store
from app.schemas import download_data_schema


def get_data(request: download_data_schema.DownloadDataRequest) -> dict:
    """
    Handles data fetching and storage for a given list of symbols.

    Args:
        request (DownloadDataRequest): A request object containing a list of symbols to fetch data for.

    Returns:
        dict: A response message indicating whether the operation was successful.

    Raises:
        HTTPException: If the data fetching or storage fails.
    """
    symbols = request.symbols

    try:
        # Attempt to fetch data for the provided symbols and store them
        fetch_and_store(symbols=symbols)
        return {"message": "Data fetched and stored."}
    except:
        return {"message": "Failed to download data. Please check your symbols and try again."}
