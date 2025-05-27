import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file (overrides existing env variables)
load_dotenv(override=True)


def init_db() -> mysql.connector.connection.MySQLConnection:
    """
    Initialize a connection to the MySQL database and ensure the required table exists.

    The function connects to the database using credentials from environment variables,
    then creates the `stock_data` table if it does not already exist.

    Returns:
        mysql.connector.connection.MySQLConnection: An active connection to the MySQL database.
    """
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
    )

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol VARCHAR(10),
            timestamp DATETIME,
            price FLOAT,
            ma_20 FLOAT,
            rsi FLOAT,
            volatility FLOAT,
            PRIMARY KEY (symbol, timestamp)
        )
    """
    )
    conn.commit()  # Commit the table creation
    cursor.close()  # Close the cursor to free resources

    return conn
