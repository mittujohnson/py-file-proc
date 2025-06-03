# your_project_name/database/db_connector.py

import psycopg2
from psycopg2 import Error
from your_project_name.config import settings

def get_db_connection():
    """Establishes and returns a PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT
        )
        print("Database connection established successfully.")
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def fetch_data_from_db(query: str) -> list:
    """
    Fetches data from the database using the given SQL query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row
              with column names as keys. Returns an empty list on error.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(query)
                # Get column names from cursor description
                columns = [desc[0] for desc in cur.description]
                data = []
                for row in cur.fetchall():
                    data.append(dict(zip(columns, row)))
                print(f"Fetched {len(data)} rows from the database.")
                return data
        return []
    except Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# Example usage (for testing purposes, not typically called directly in production)
if __name__ == "__main__":
    sample_query = "SELECT id, name, email FROM users LIMIT 5;" # Replace with your table and columns
    data = fetch_data_from_db(sample_query)
    if data:
        for row in data:
            print(row)