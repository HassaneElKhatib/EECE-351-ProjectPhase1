import sqlite3

def connect_to_database() -> sqlite3.Connection:
    """Connects to the SQLite database."""
    return sqlite3.connect("auboutique.db")

def create_tables(conn: sqlite3.Connection):
    """Creates necessary tables in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                address VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products(
                username VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL PRIMARY KEY,
                picture VARCHAR(255) NOT NULL,
                price FLOAT(4) NOT NULL,
                description TEXT,
                Quantity Integer NOT NULL,
                FOREIGN KEY (username) REFERENCES Users(username)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Purchases(
                id Integer Primary Key AutoIncrement,
                product_name VARCHAR(255) NOT NULL,
                buyer_username VARCHAR(255) NOT NULL,
                seller_username VARCHAR(255) NOT NULL,
                FOREIGN KEY (product_name) REFERENCES Products(name),
                FOREIGN KEY (buyer_username) REFERENCES Users(username),
                FOREIGN KEY (seller_username) REFERENCES Users(username)
            )
        """)
        conn.commit()
        print("[SERVER] Tables created successfully.")
    except sqlite3.Error as e:
        print(f"[SERVER] Error creating tables: {e}")
