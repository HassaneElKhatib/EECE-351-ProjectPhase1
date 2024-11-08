from response import HttpResponse
import socket
import sqlite3
import user
import product
import json
import threading
import sys
from request import HttpRequest

online_users = {}

def connectToDatabase() -> sqlite3.Connection:
    """
    Connects to database

    :return: connection to database
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect("auboutique.db")
    return conn


def createTables(conn: sqlite3.Connection):
    """
    Creates 3 tables: Users, Products and Purchases and stores them in the database

    :param conn: connects to database
    :type conn: sqlite3.Connection
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""Create Table Users(
                    name varchar(255) NOT NULL,
                    email varchar(255) NOT NULL Unique,
                    address varchar(255) NOT NULL, 
                    username varchar(255) NOT NULL Primary Key,
                    password varchar(255) NOT NULL
                    )""")
        cursor.execute("""Create Table Products(
                    username varchar(255) NOT NULL,
                    name varchar(255) NOT NULL Primary Key,
                    picture varchar(255) NOT NULL,
                    price Float(4) NOT NULL,
                    description varchar(65535),
                    Foreign Key (username) References Users(username)
                    )""")
        cursor.execute("""Create Table Purchases(
                       product_name varchar(255) NOT NULL,
                       buyer_username varchar(255) NOT NULL,
                       seller_username varchar(255) NOT NULL Primary Key,
                       Foreign Key(product_name) References Products(name),
                       Foreign Key (buyer_username) References Users(username),
                       Foreign Key (seller_username) References Users(username)
                       )""")
    except sqlite3.Error as e:
        print(e)

def check_online(request):
    """
    Checks if a user is online

    :param request: HTTP request from the client
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    username_to_check = body.get("username")
    if username_to_check in online_users:
        message=f"{username_to_check} is online"
    else:
        message=f"{username_to_check} is offline"
    response.set_header("Content-Type", "application/json")
    response.set_status_code(200)
    response.set_body(json.dumps({"message": message}))
    return response.build_response()

def send_message(request):
    """
    Sends a message to another user, if the user is online
    """
    response = HttpResponse()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    recipient_username = body.get("recipient")
    message = body.get("message")
    sender_username = body.get("sender")
    command = body.get("command", None)
    if recipient_username in online_users:
        recipient_socket = online_users[recipient_username]
        try:
            if command == "QUIT":
                message_body = json.dumps({"command": "QUIT", "sender": sender_username})
            else:
                message_body = json.dumps({"direct_message": f"Message from {sender_username}: {message}"})
            http_response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{message_body}"
            recipient_socket.sendall(http_response.encode())
            response.set_body(json.dumps({"message": "Message sent successfully"}))
            response.set_status_code(200)
        except Exception as e:
            print(f"Error sending message to {recipient_username}: {e}")
            response.set_body(json.dumps({"message": "Failed to send message"}))
            response.set_status_code(500)
    else:
        response.set_body(json.dumps({"message": "Recipient is offline"}))
        response.set_status_code(404)
    response.set_header("Content-Type", "application/json")
    return response.build_response()

def logout(body):
    """
    Logs out the user and marks the user as offline

    :param body: body of the HTTP response
    :type body: dict
    """
    username = body.get("username")
    if username in online_users:
        del online_users[username]
        print(f"{username} logged out.")

def getProductsFromUser(request):
    """
    Gets the products from a specific user by accessing the database

    :param request: request
    :type request: HTTPRequest
    :return: response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    username = body.get("username")
    try:
        if username is None:
            response.set_body(json.dumps({"message": "Username is required"}))
            response.set_status_code(400)
            return response.build_response()
        products = product.getProducts(conn, username)
        if products:
            product_list = [
                {"username": row[0], "name": row[1], "picture": row[2], "price": row[3], "description": row[4]}
                for row in products
            ]
            response.set_header("Content-Type", "application/json")
            response.set_body(json.dumps({"products": product_list}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps(
                {"message": "No products found for the user"}))
            response.set_status_code(404)
    except Exception as e:
        print(f"[SERVER] Error in getProductsFromUser: {e}")
        response.set_body(json.dumps({"message": "An error occurred"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()



def getAllProducts():
    """
    Gets all the products from the database

    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    try:
        products = product.getAllProducts(conn)
        if products:
            product_list = [
                {"username": row[0], "name": row[1], "picture": row[2], "price": row[3], "description": row[4]}
                for row in products
            ]
            response.set_header("Content-Type", "application/json")
            response.set_body(json.dumps({"products": product_list}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps({"message": "No products found"}))
            response.set_status_code(404)
    except Exception as e:
        print(f"[SERVER] Error in getAllProducts: {e}")
        response.set_body(json.dumps({"message": "An error occurred"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()


def buyProducts(request):
    """
    Buys a product from a user

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    name = body.get("name")
    buyer_username = body.get("username")
    try:
        bought = product.buyProducts(name, buyer_username,conn)
        response.set_header("Content-Type","application/json")
        if bought:
            response.set_body(json.dumps({"message":"Product bought successfully\nGet it from the registrar in 5 days"}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps({"message": "Failed to buy product"}))
            response.set_status_code(400)
    except Exception as e:
        print(e)
        response.set_body(json.dumps(
            {"message": "Error occured while buying product"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()


def addProduct(request):
    """
    Adds a product from the user to the database

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    name = body.get("name")
    username = body.get("username")
    picture = body.get("picture")
    price = body.get("price")
    description = body.get("description")
    try:
        added = product.insertProducts(username, name, picture, price, description, conn)
        response.set_header("Content-Type", "application/json")
        if added:
            response.set_body(json.dumps(
                {"message": "Product added successfully"}))
            response.set_status_code(201)
        else:
            response.set_body(json.dumps({"message": "Failed to add product"}))
            response.set_status_code(400)
    except Exception as e:
        print(f"[SERVER] Error in addProduct: {e}")
        response.set_body(json.dumps(
            {"message": "Error occurred while adding product"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()


def removeProduct(request):
    """
    Removes a product from the database

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    name = body.get("name")
    username = body.get("username")
    try:
        removed = product.removeProducts(username, name, conn)
        response.set_header("Content-Type", "application/json")
        if removed:
            response.set_body(json.dumps(
                {"message": "Product removed successfully"}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps(   
                {"message": "Failed to remove product"}))
            response.set_status_code(400)
    except Exception as e:
        print(f"[SERVER] Error in removeProduct: {e}")
        response.set_body(json.dumps(
            {"message": "Error occurred while removing product"}))
        response.set_status_code(500)
    finally:
        conn.close()
        
    return response.build_response()


def updateProduct(request):
    """
    Updates a product from the database

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    username = body.get("username")
    name = body.get("name")
    picture = body.get("picture")
    price = body.get("price")
    description = body.get("description")
    try:
        updated = product.updateProducts(username,name, picture, price, description, conn)
        response.set_header("Content-Type", "application/json")
        if updated:
            response.set_body(json.dumps(
                {"message": "Product updated successfully"}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps(
                {"message": "Failed to update product"}))
            response.set_status_code(400)
    except Exception as e:
        print(f"[SERVER] Error in updateProduct: {e}")
        response.set_body(json.dumps(
            {"message": "Error occurred while updating product"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()


def viewBuyers(request):
    """
    Views the list of buyers of a user

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = json.loads(parsed_request["body"])
    seller_username = body.get("username")
    try:
        buyers = product.viewBuyers(seller_username, conn)
        response.set_header("Content-Type", "application/json")
        if buyers is not None:
            response.set_body(json.dumps({"buyers": buyers}))
            response.set_status_code(200)
        else:
            response.set_body(json.dumps({"message": "No buyers found"}))
            response.set_status_code(404)
    except Exception as e:
        print(f"[SERVER] Error in viewBuyersEndpoint: {e}")
        response.set_body(json.dumps({"message": "An error occurred"}))
        response.set_status_code(500)
    finally:
        conn.close()
    return response.build_response()

def register(request):
    """
    Registers the user into the server

    :param request: HTTP request
    :type request: HTTPRequest
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = parsed_request["body"]
    body = json.loads(body)
    try:
        registered = user.register(body["name"], body["email"], body["address"],
                                   body["username"], body["password"], conn)
        response.set_header("Content-Type", "application/json")
        if registered:
            response.set_body(json.dumps(
                {"message": "Registration successful"}))
            response.set_status_code(201)
        else:
            response.set_body(json.dumps({"message": "Invalid credentials"}))
            response.set_status_code(404)
    except Exception as e:
        response.set_body(json.dumps({"message": "Error occured"}))
        response.set_status_code(404)
    conn.close()
    return response.build_response()

def login(request, client_socket):
    """
    Logins the user into the boutique

    :param request: HTTP request
    :type request: HTTPRequest
    :param client_socket: connects to client socket
    :type client_socket: socket.socket
    :return: HTTP response
    :rtype: HTTPResponse
    """
    response = HttpResponse()
    conn = connectToDatabase()
    parsed_request = HttpRequest.parse_http_request(request)
    body = parsed_request["body"]
    body = json.loads(body)
    try:
        logged_in = user.login(body["username"], body["password"], conn)
        response.set_header("Content-Type", "application/json")
        if logged_in:
            response.set_body(json.dumps(
                {"message": "Login successful"}))
            response.set_status_code(200)
            online_users[body["username"]] = client_socket
        else:
            response.set_body(json.dumps({"message": "Login failed"}))
            response.set_status_code(401)
    except Exception as e:
        response.set_body(json.dumps({"message": "Error occurred"}))
        response.set_status_code(400)
    conn.close()
    return response.build_response()


def client_handler(client_socket):
    """
    Handles the client's functionalities

    :param client_socket: connects to client socket
    :type client_socket: socket.socket
    """
    conn = connectToDatabase()
    createTables(conn)
    alias = None
    while True:
        try:
            request = client_socket.recv(4096).decode()
            if not request:
                break
            http_packet = HttpRequest.parse_http_request(request)
            uri = http_packet.get("uri")
            if uri == "/register":
                response = register(request)
            elif uri == "/login":
                response = login(request, client_socket)
            elif uri == "/logout":
                body = json.loads(HttpRequest.parse_http_request(request)["body"])
                logout(body)
                response = "HTTP/1.1 200 OK\r\n\r\nLogout successful"
            elif uri == "/view_all_products":
                response = getAllProducts()
            elif uri == "/get_user_products":
                response = getProductsFromUser(request)
            elif uri == "/buy_product":
                response = buyProducts(request)
            elif uri == "/add_product":
                response = addProduct(request)
            elif uri == "/view_buyers":
                response = viewBuyers(request)
            elif uri == "/remove_product":
                response = removeProduct(request)
            elif uri == "/update_product":
                response = updateProduct(request)
            elif uri == "/check_online":
                response = check_online(request)
            elif uri == "/send_message":
                response = send_message(request)
            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nInvalid endpoint".encode()
            client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Error handling client request: {e}")
            client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nAn error occurred.".encode())
            break
    client_socket.close()

def logout(body):
    """
    Logs out a user and marks him as offline

    :param body: HTTP body
    :type body: dict
    """
    username = body.get("username")
    if username in online_users:
        del online_users[username]

def start_server(host, port):
    """
    Starts the server

    :param host: IP address of the server, defaults to "0.0.0.0"
    :type host: str, optional
    :param port: Host port, defaults to 30300
    :type port: int, optional
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = int(sys.argv[1])
    start_server(HOST,PORT)

