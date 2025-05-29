from app.utils.store_data import fetch_and_store
from typing import List


def get_data(symbols: List[str]) -> dict:
    """
    Handles data fetching and storage for a given list of symbols.

    Args:
        symbols: Containing a list of symbols to fetch data for.

    Returns:
        dict: A response message indicating whether the operation was successful or failed.
    """
    try:
        # Attempt to fetch data for the provided symbols and store them
        fetch_and_store(symbols=symbols)
        return {"message": "Data fetched and stored."}
    except:
        return {
            "message": "Failed to download data. Please check your symbols and try again."
        }
