import yfinance as yf
import pandas as pd
from app.db.mysql import init_db


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators for a given price DataFrame.

    Indicators:
        - 20-period Moving Average (ma_20)
        - Relative Strength Index (RSI)
        - 20-period Rolling Standard Deviation (Volatility)

    Args:
        df (pd.DataFrame): DataFrame containing a 'price' column.

    Returns:
        pd.DataFrame: DataFrame with added indicator columns.
    """
    df["ma_20"] = df["price"].rolling(window=20).mean()
    df["rsi"] = compute_rsi(df["price"])
    df["volatility"] = df["price"].rolling(window=20).std()
    return df


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Compute the Relative Strength Index (RSI) for a given price series.

    Args:
        series (pd.Series): Series of prices.
        period (int, optional): Number of periods to use for calculation. Defaults to 14.

    Returns:
        pd.Series: RSI values for the input series.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def get_scalar_value(val) -> float | None:
    """
    Convert a value or a single-element Series to a float, if possible.

    Args:
        val: A float or a pandas Series containing one float element.

    Returns:
        float | None: A float value or None if the input is invalid or missing.
    """
    if isinstance(val, pd.Series):
        return float(val.iloc[0]) if not val.empty and pd.notnull(val.iloc[0]) else None
    return float(val) if pd.notnull(val) else None


def fetch_and_store(symbols: list[str]) -> None:
    """
    Fetches real-time stock data from Yahoo Finance for a list of symbols,
    calculates technical indicators, and stores the results in a MySQL database.

    Args:
        symbols (list[str]): List of stock ticker symbols.

    Raises:
        ValueError: If data for a symbol could not be retrieved.
        Exception: For any database operation errors.
    """
    conn = init_db()
    cursor = conn.cursor()

    for symbol in symbols:
        # Download 1-day, 1-minute interval data
        data = yf.download(symbol, period="1d", interval="1m")

        if data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        # Prepare DataFrame with price and indicators
        df = pd.DataFrame(data)
        df = df[["Close"]].rename(columns={"Close": "price"})
        df = calculate_indicators(df)

        # Insert each row of processed data into the database
        for i, row in df.iterrows():
            try:
                timestamp = i.to_pydatetime() if hasattr(i, "to_pydatetime") else i
                price = get_scalar_value(row["price"])
                ma_20 = get_scalar_value(row["ma_20"])
                rsi = get_scalar_value(row["rsi"])
                volatility = get_scalar_value(row["volatility"])

                cursor.execute(
                    """
                    INSERT INTO stock_data (symbol, timestamp, price, ma_20, rsi, volatility)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (symbol, timestamp, price, ma_20, rsi, volatility),
                )
            except Exception as e:
                raise e

    # Finalize transaction and close connection
    conn.commit()
    conn.close()
