import sqlite3

def insertProducts(username, name, picture, price, description, conn: sqlite3.Connection):
    """
    Inserts the user's product to the database given the user's username, name of the product, picture of
    the product, price of the product and description of the  product

    :param username: user's username
    :type username: str
    :param name: product name
    :type name: str
    :param picture: product picture
    :type picture: str
    :param price: product price
    :type price: float
    :param description: product description
    :type description: str
    :param conn: connects to database
    :type conn: sqlite3.Connection
    :return: `True` if product was added to the database, `False` otherwise
    :rtype: bools
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (username,name, picture, price, description) VALUES (?, ?, ?, ?, ?)",
            (username,name, picture, price, description)
        )
        conn.commit()
        print("[SERVER] Product Successfully Inserted!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error inserting product: {e}")
        return False

def buyProducts(name, buyer_username, conn: sqlite3.Connection):
    """
    Buys the product of a certain user by giving the name of the product
    and the buyer's username

    :param name: product name
    :type name: str
    :param buyer_username: user's username
    :type buyer_username: str
    :param conn: connects to database
    :type conn: sqlite3.Connection
    :return: `True` if product was bought, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        cursor.execute("Select username from Products where name = ?",(name,))
        seller = cursor.fetchone()
        if not seller:
            print("[SERVER] Product Not Found")
            return False
        seller_username = seller[0]
        cursor.execute("Insert into Purchases (product_name, buyer_username, seller_username) values (?,?,?)", (name, buyer_username, seller_username))
        conn.commit()   
        cursor.execute("DELETE FROM Products WHERE name = ?", (name,))
        conn.commit()
        print("[SERVER] Product Successfully bought and recorded in Purchases!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error buying product: {e}")
        return False

def removeProducts(username, name, conn: sqlite3.Connection):
    """
    Removes a product from the database given the user's username
    and the product's name

    :param username: user's username
    :type username: str
    :param name: product name
    :type name: str
    :param conn: connects to database
    :type conn: sqlite3.Connection
    :return: `True` if product was deleted and removed from database, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        cursor.execute("Select username from Products where username = ?",(username,))
        user = cursor.fetchone()
        if user[0] != username:
            return False
        cursor.execute("DELETE FROM Products WHERE name = ?", (name,))
        conn.commit()
        print("[SERVER] Product Successfully Removed!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error removing product: {e}")
        return False

def updateProducts(username, name, picture, price, description, conn: sqlite3.Connection):
    """
    Updates the information of a product by giving the username, the new name,
    the new picture, the new price and the new description

    :param username: user's username
    :type username: str
    :param name: product name
    :type name: str
    :param picture: product picture
    :type picture: str
    :param price: product price
    :type price: float
    :param description: product description
    :type description: str
    :param conn: connect to database
    :type conn: sqlite3.Connection
    :return: `True` if the product is updated, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()
        cursor.execute("Select username from Products where username = ?",(username,))
        user = cursor.fetchone()
        if user[0] != username:
            return False
        cursor.execute(
                "UPDATE Products SET price = ?, description = ?, picture = ? WHERE name = ?",
                (price, description,picture, name)
            )
        conn.commit()
        print("[SERVER] Product Successfully Updated!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error updating product: {e}")
        return False

def getProducts(conn: sqlite3.Connection, username: str):
    """
    Get the products listed by a specific user, takes as input the 
    user's username

    :param conn: connect to database
    :type conn: sqlite3.Connection
    :param username: user's username
    :type username: str
    :return: the products list of the user if there exists, else returns `None`
    :rtype: List
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products WHERE username = ?", (username,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[SERVER] Error retrieving products for user {username}: {e}")
        return None

def getAllProducts(conn: sqlite3.Connection):
    """
    Get all the products of the website

    :param conn: connect to database
    :type conn: sqlite3.Connection
    :return: the products list of the boutique, else returns `None`
    :rtype: List
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[SERVER] Error retrieving all products: {e}")
        return None

def viewBuyers(seller_username, conn: sqlite3.Connection):
    """
    Gets the list of buyers of a user given the user's username

    :param seller_username: seller's username
    :type seller_username: str
    :param conn: connect to database
    :type conn: sqlite3.Connection
    :return: list of buyers
    :rtype: List
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT buyer_username FROM Purchases WHERE seller_username = ?", (seller_username,))
        buyers = cursor.fetchall()
        buyer_list = [row[0] for row in buyers]
        return buyer_list
    except sqlite3.Error as e:
        print(f"[SERVER] Error retrieving buyers: {e}")
        return None