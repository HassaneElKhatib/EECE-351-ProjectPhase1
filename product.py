import sqlite3

def insertProducts(username, name, picture, price, description, quantity, conn: sqlite3.Connection):
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
            "INSERT INTO Products (username,name, picture, price, description, quantity) VALUES (?, ?, ?, ?, ?, ?)",
            (username,name, picture, price, description, quantity)
        )
        conn.commit()
        print("[SERVER] Product Successfully Inserted!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error inserting product: {e}")
        return False

def buyProducts(name, buyer_username, quantity_to_buy, conn: sqlite3.Connection, online_users):
    """
    Buys a specified quantity of a product. If the quantity matches the stock, 
    the product is removed. Otherwise, the quantity is decremented.

    :param name: product name
    :type name: str
    :param buyer_username: buyer's username
    :type buyer_username: str
    :param quantity_to_buy: quantity to buy
    :type quantity_to_buy: int
    :param conn: connects to database
    :type conn: sqlite3.Connection
    :param online_users: dictionary of online users
    :type online_users: dict
    :return: `True` if the operation is successful, `False` otherwise
    :rtype: bool
    """
    try:
        cursor = conn.cursor()

        # Fetch product information
        cursor.execute("SELECT username, Quantity FROM Products WHERE name = ?", (name,))
        product = cursor.fetchone()

        if not product:
            print("[SERVER] Product Not Found")
            return False

        seller_username, current_quantity = product

        # Validate quantity
        if quantity_to_buy > current_quantity:
            print("[SERVER] Requested quantity exceeds available stock")
            return False

        # Check if buyer is a valid online user
        if buyer_username not in online_users:
            print("[SERVER] Buyer is not a valid online user")
            return False

        if buyer_username == seller_username:
            print("[SERVER] Buyer cannot be the same as the seller")
            return False

        cursor.execute(
            "INSERT INTO Purchases (product_name, buyer_username, seller_username) VALUES (?, ?, ?)",
            (name, buyer_username, seller_username),
        )

        if quantity_to_buy == current_quantity:
            cursor.execute("DELETE FROM Products WHERE name = ?", (name,))
        else:
            cursor.execute(
                "UPDATE Products SET Quantity = Quantity - ? WHERE name = ?",
                (quantity_to_buy, name),
            )

        conn.commit()
        print("[SERVER] Product purchase recorded and stock updated successfully!")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error buying product: {e}")
        return False


def removeProducts(username, name, conn: sqlite3.Connection, client_address, online_users):
    """
    Removes a product from the database if the requesting user matches the product owner.

    :param username: user's username
    :param name: product name
    :param conn: database connection
    :param client_address: (IP, Port) of the client
    :param online_users: dictionary of online users
    :return: True if the product is deleted, False otherwise
    """
    try:
        if username not in online_users or online_users[username]["ip"] != client_address[0]:
            print("[SERVER] Unauthorized access attempt for product removal.")
            return False

        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Products WHERE name = ?", (name,))
        product = cursor.fetchone()

        if not product or product[0] != username:
            print("[SERVER] Product not found or user is not the owner.")
            return False

        cursor.execute("DELETE FROM Products WHERE name = ? AND username = ?", (name, username))
        conn.commit()
        print("[SERVER] Product successfully removed.")
        return True
    except sqlite3.Error as e:
        print(f"[SERVER] Error removing product: {e}")
        return False




def updateProducts(username, name, picture, price, description, quantity, conn: sqlite3.Connection, client_address, online_users):
    """
    Updates product information if the requesting user matches the product owner.

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
    :param quantity: product quantity
    :type quantity: int
    :param conn: database connection
    :type conn: sqlite3.Connection
    :param client_address: (IP, Port) of the client
    :type client_address: tuple
    :param online_users: dictionary of online users
    :type online_users: dict
    :return: True if product updated successfully, False otherwise
    :rtype: bool
    """
    try:
        if username not in online_users or online_users[username]["ip"] != client_address[0] or online_users[username]["port"] != client_address[1]:
            print("[SERVER] Unauthorized access attempt for product update.")
            return False

        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Products WHERE name = ?", (name,))
        product = cursor.fetchone()

        if not product or product[0] != username:
            print("[SERVER] Product not found or user is not the owner.")
            return False

        cursor.execute(
            "UPDATE Products SET price = ?, description = ?, picture = ?, quantity = ? WHERE name = ?",
            (price, description, picture, quantity, name),
        )
        conn.commit()
        print("[SERVER] Product successfully updated.")
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
    Gets the list of buyers of a user's products along with the product name and quantity.

    :param seller_username: Seller's username
    :type seller_username: str
    :param conn: Database connection
    :type conn: sqlite3.Connection
    :return: List of buyers, product names, and quantities
    :rtype: List[Dict]
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Purchases.buyer_username, Purchases.product_name, COUNT(Purchases.product_name) AS quantity
            FROM Purchases
            WHERE Purchases.seller_username = ?
            GROUP BY Purchases.buyer_username, Purchases.product_name
        """, (seller_username,))
        buyers = cursor.fetchall()
        buyer_list = [
            {"buyer_username": row[0], "product_name": row[1], "quantity": row[2]}
            for row in buyers
        ]
        return buyer_list
    except sqlite3.Error as e:
        print(f"[SERVER] Error retrieving buyers: {e}")
        return []
