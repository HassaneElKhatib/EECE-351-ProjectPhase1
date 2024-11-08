import socket
import sys
import json
import threading
from request import HttpRequest
from response import HttpResponse
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
PORT = int(sys.argv[1])
clientSocket.connect((IP, PORT))

current_username = None  

def register(body: dict):
    """
    Build the HTTP request for registration

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/register")
    request.set_body(json.dumps(body))
    return request.build_request()

def login(body: dict):
    """
    Build the HTTP request for login

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/login")
    request.set_body(json.dumps(body))
    return request.build_request()

def add_product(body: dict):
    """
    Build the HTTP request for adding a product

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/add_product")
    request.set_body(json.dumps(body))
    return request.build_request()

def remove_product(body: dict):
    """
    Build the HTTP request for removing a product

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="DELETE", url="/remove_product")
    request.set_body(json.dumps(body))
    return request.build_request()

def buy_product(body: dict):
    """
    Build the HTTP request for buying a product

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/buy_product")
    request.set_body(json.dumps(body))
    return request.build_request()

def view_buyers(body: dict):
    """
    Build the HTTP request for viewing buyers

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/view_buyers")
    request.set_body(json.dumps(body))
    return request.build_request()

def view_all_products():
    """
    Build the HTTP request for viewing all products

    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="GET", url="/view_all_products")
    return request.build_request()

def view_user_products(body: dict):
    """
    Build the HTTP request for viewing a user's products

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/get_user_products")
    request.set_body(json.dumps(body))
    return request.build_request()

def update_product(body: dict):
    """
    Build the HTTP request for updating a product

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="PUT", url="/update_product")
    request.set_body(json.dumps(body))
    return request.build_request()

def check_online(body: dict):
    """
    Build the HTTP request for checking if a user is online

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/check_online")
    request.set_body(json.dumps(body))
    return request.build_request()

def send_message_request(body: dict):
    """
    Build the HTTP request for sending a message 

    :param body: the message of the HTTP request
    :type body: dict
    :return: HTTP request
    :rtype: HTTPRequest
    """
    request = HttpRequest(method="POST", url="/send_message")
    request.set_body(json.dumps(body))
    return request.build_request()

def receive_messages():
    """
    Handles receiving messages between users
    """
    global other_user_quit
    while True:
        try:
            message = clientSocket.recv(4096).decode()
            if message:
                if message.startswith('HTTP'):
                    parsed_response = HttpResponse.parse_http_response(message)
                    if parsed_response and "body" in parsed_response:
                        response_body = json.loads(parsed_response["body"])
                        if "command" in response_body and response_body["command"] == "QUIT":
                            sender = response_body.get("sender")
                            print(f"\n{sender} has exited the chat.\n")
                            other_user_quit = True  
                        elif "direct_message" in response_body:
                            print(f"\n{response_body['direct_message']}\n")
                        elif "message" in response_body:
                            print(f"\n{response_body['message']}\n")
                        elif "buyers" in response_body:
                            print("Buyers:", ", ".join(response_body["buyers"]))
                        elif "products" in response_body:
                            for product in response_body["products"]:
                                print(f"Username: {product['username']}, Name: {product['name']}, Price: {product['price']}, Description: {product['description']}")
                        else:
                            print("Unknown response format:", response_body)
                    else:
                        print("Failed to parse server response")
                else:
                    print(f"\n{message}\n")
            else:
                print("Server closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def handleOption(option, socket: socket.socket):
    """
    Handles the registration and login options

    :param option: Checks if it is login or registration
    :type option: int
    :param socket: connects to the socket
    :type socket: socket.socket
    :return: `register` if option is 1, `login` if option is 2, else returns `None`
    :rtype: str
    """
    global current_username
    if option == 1:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        body = {"name": name, "email": email,
                "address": address, "username": username, "password": password}
        registration_packet = register(body)
        socket.sendall(registration_packet.encode())
        return "register"
    elif option == 2:
        name = input("Enter your username: ")
        password = input("Enter your password: ")
        body = {"username": name, "password": password}
        login_packet = login(body)
        socket.sendall(login_packet.encode())
        current_username = name
        return "login"
    else:
        print("Invalid option")
        return None
    

def logout():
    """
    Logs out the user

    :return: HTTP request
    :rtype: HTTPRequest
    """
    global current_username
    body = {"username": current_username}
    request = HttpRequest(method="POST", url="/logout")
    request.set_body(json.dumps(body))
    current_username = None 
    return request.build_request()


def getOption(socket: socket.socket):
    """
    Gets the user's option to register or login

    :param socket: connects to socket
    :type socket: socket.socket
    :return: `register` if user wants to register, `login` if user wants to login
    :rtype: str
    """
    valid = None
    while not valid:
        option = int(
            input("Choose an option:\n[1] Register\n[2] Login\nOption: "))
        valid = handleOption(option, socket)
    return valid

def handleOptions(option, socket: socket.socket):
    """
    Handles different product options as well as the options to check if online, message 
    other users and logout and sends the HTTP requests to the server

    :param option: Chooses an option
    :type option: int
    :param socket: connects to socket
    :type socket: socket.socket
    :return: Url
    :rtype: str
    """
    if option == 1:
        view_all_packet = view_all_products()
        socket.sendall(view_all_packet.encode())
        return "view_all_products"
    elif option == 2:
        username = input(
            "Enter the username of the user you wish to view their products: ")
        body = {"username": username}
        view_user_products_packet = view_user_products(body)
        socket.sendall(view_user_products_packet.encode())
        return "get_user_products"
    elif option == 3:
        username = input(
            "Enter your username to view buyers of your products: ")
        body = {"username": username}
        view_buyers_packet = view_buyers(body)
        socket.sendall(view_buyers_packet.encode())
        return "view_buyers"
    elif option == 4:
        username = current_username
        name = input("Enter product name: ")
        picture = input("Enter the file path for the product image: ")
        price = float(input("Enter product price: "))
        description = input("Enter product description: ")
        body = {"name": name, "username": username, "picture": picture,
                "price": price, "description": description}
        add_product_packet = add_product(body)
        socket.sendall(add_product_packet.encode())
        return "add_product"
    elif option == 5:
        username = current_username
        name = input("Enter the name of the product to remove: ")
        body = {"name": name, "username": username}
        remove_product_packet = remove_product(body)
        socket.sendall(remove_product_packet.encode())
        return "remove_product"
    elif option == 6:
        username = current_username
        name = input("Enter the name of the product to buy: ")
        body = {"name": name, "username": username}
        buy_product_packet = buy_product(body)
        socket.sendall(buy_product_packet.encode())
        return "buy_product"
    elif option == 7:
        username = current_username
        name = input("Enter the name of the Product you want to update: ")
        picture = input("Enter the new file path for the product image: ")
        price = float(input("Enter the new product price: "))
        description = input("Enter the new product description: ")
        body = {"username": username, "name": name, "picture": picture,
                "price": price, "description": description}
        update_product_packet = update_product(body)
        socket.sendall(update_product_packet.encode())
        return "update_product"
    elif option == 8:
        username_to_check = input("Enter the username to check if online: ")
        body = {"username": username_to_check}
        check_online_packet = check_online(body)
        socket.sendall(check_online_packet.encode())
        return "check_online"
    elif option == 9:
        print("Messaging mode activated. Type 'QUIT' to exit.")
        recipient = input("Enter the recipient's username: ")
        global other_user_quit
        other_user_quit = False  
        while True:
            message = input("Enter your message: ")
            if message.upper() == "QUIT":
                body = {"recipient": recipient, "message": "QUIT", "sender": current_username, "command": "QUIT"}
                send_message_packet = send_message_request(body)
                socket.sendall(send_message_packet.encode())
                print("Exiting messaging mode.")
                break
            else:
                body = {"recipient": recipient, "message": message, "sender": current_username}
                send_message_packet = send_message_request(body)
                socket.sendall(send_message_packet.encode())
            if other_user_quit:
                print(f"{recipient} has exited the chat.")
                break
        return "send_message"
    elif option == 10:
        logout_packet = logout()
        socket.sendall(logout_packet.encode())
        print("Logged out successfully.")
        return "logout"
    else:
        print("Invalid option")
        return None

def getOptions(socket: socket.socket):
    """
    Gets different product options from the user with the addition
    to message, check for activity and logout

    :param socket: connects to socket
    :type socket: socket.socket
    :return: the options
    :rtype: str
    """
    valid = None
    while not valid:
        time.sleep(0.5)
        option = int(input(
            "Choose an option:\n[1] View Products \n[2] View Users' Products \n[3] View Buyers\n[4] Add Product\n[5] Remove Product\n[6] Buy Product\n[7] Update Product\n[8] Check Online\n[9] Send Message\n[10] Logout\nOption: "))
        valid = handleOptions(option, socket)
        if valid == "logout":
            break
    return valid


def main():     
    """
    Handles the main functionality of the client
    """
    print("Welcome to AUBoutique!")
    while True:
        getOption(clientSocket)
        response = clientSocket.recv(4096).decode()
        parsed_response = HttpResponse.parse_http_response(response)
        res = json.loads(parsed_response["body"])["message"]
        if res == "Registration successful":
            print(res)

        elif res == "Login successful":
            print(res)
            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            break
        else:
            print("Enter correct login credentials")
    while True:
        result=getOptions(clientSocket) 
        if result=="logout":
            break
main()