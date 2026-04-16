import os
import psycopg2
from dotenv import load_dotenv

# inputing some env variable .env to connect to db
load_dotenv()


def test_connection():
    try:
        # call postgresql connection using psycopg2 library
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("[SUCCESS] Connection to the database was successful!")

        # close connection after testing
        conn.close()

    except Exception as e:
        print(
            f"[ERROR] connection failed: {e}")


if __name__ == "__main__":
    test_connection()
