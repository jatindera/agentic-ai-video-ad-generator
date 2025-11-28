import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname="aivideodb",      # change to your DB name
            user="aivideoadmin",        # change if needed
            password="12345678",
            host="localhost",
            port="5432"             # default PostgreSQL port
        )

        print("✔ Successfully connected to PostgreSQL!")

        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()

        print("PostgreSQL version:", version)

        cur.close()
        conn.close()

    except OperationalError as e:
        print("✘ Unable to connect!")
        print(e)

if __name__ == "__main__":
    test_connection()
