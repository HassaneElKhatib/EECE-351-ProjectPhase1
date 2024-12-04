import bcrypt
import sqlite3



def register(name, email, address, username, password, conn: sqlite3.Connection):
    """
    Registers the name, email, address, username and the encrypted password 
    of a given user and saves them in the Users database

    :param name: user's name
    :type name: str
    :param email: user's email
    :type email: str
    :param address: user's address
    :type address: str
    :param username: user's username
    :type username: str
    :param password: user's password
    :type password: str
    :param conn: connects to the database
    :type conn: sqlite3.Connection
    :return: `True` if registration successful, `False` otherwise 
    :rtype: bool
    """
    try:
        cursor = conn.cursor()

        # Hash the password (if bcrypt is used)
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Insert into the Users table
        cursor.execute(
            """
            INSERT INTO Users (name, email, address, username, password)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, address, username, hashed_password),
        )
        conn.commit()  # Commit the transaction
        print("[SERVER] User registered successfully!")
        return True
    except sqlite3.IntegrityError as e:
        print(f"[SERVER] Integrity error: {e}")
        return False
    except sqlite3.Error as e:
        print(f"[SERVER] Database error: {e}")
        return False
    finally:
        cursor.close()

def login(username, password, conn: sqlite3.Connection):
    """
    Logs in the user to the site by checking the username in the 
    database as well as the encrypted password.

    :param username: user's username
    :type username: str
    :param password: user's password
    :type password: str
    :param conn: connects to the database 
    :type conn: sqlite3.Connection
    :return: `True` if login successful, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[1]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode() 
            if bcrypt.checkpw(password.encode(), stored_password):
                print(f"[SERVER] User '{username}' logged in successfully.")
                return True
            else:
                print(f"[SERVER] Incorrect password for user '{username}'.")
        else:
            print(f"[SERVER] User '{username}' not found.")
        return False
    except sqlite3.Error as e:
        print(f"[SERVER] Database error during login: {e}")
        return False
