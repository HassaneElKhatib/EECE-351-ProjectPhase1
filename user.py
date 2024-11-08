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
    cursor = conn.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    if name and email and address and username and password:
        try:
            cursor.execute("Insert into Users (name, email, address, username, password) values (?,?,?,?,?)",
                           (name, email, address, username, hashed_password))
            conn.commit()
            cursor.close()
            print("[SERVER] Successfully Registered User!")
            return True
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return False


def login(username, password, conn: sqlite3.Connection):
    """
    Logs in the user to the site by checking the username in the 
    database as well as the encrypted password

    :param username: user's username
    :type username: str
    :param password: user's password
    :type password: str
    :param conn: connects to the database 
    :type conn: sqlite3.Connection
    :return: `True` if login sucessful, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        data = cursor.execute(
            f"select username, password from Users where username='{username}'")
        user = data.fetchone()
        if user:
            if bcrypt.checkpw(password.encode(), user[1]):
                cursor.close()
                print("[SERVER] Successfully logged in!")
                return True
        else:
            return None
    except sqlite3.Error as e:
        print(e)
    return False