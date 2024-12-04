import socket
import threading
from Authentication import *
from ProductHandlers import *
from Buyers import view_buyers_handler
from Database import connect_to_database, create_tables
from request import *
from response import *


def add_cors_headers(response):
    """Adds CORS headers to all responses."""
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.set_header("Access-Control-Allow-Headers", "Content-Type")

def handle_options_request(client_socket):
    """Handles CORS preflight (OPTIONS) requests."""
    response = (
        "HTTP/1.1 204 No Content\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: POST, GET, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Access-Control-Max-Age: 86400\r\n"
        "\r\n"
    )
    client_socket.sendall(response.encode())


def handle_client(client_socket, address):
    print(f"[SERVER] Connected to {address}")
    try:
        while True:
            request = client_socket.recv(4096).decode()
            if not request:
                print(f"[SERVER] Client {address} disconnected.")
                break
            print(f"[DEBUG] Incoming request: {request}")

            if request.startswith("OPTIONS"):
                handle_options_request(client_socket)
                continue

            response = None
            if "/register" in request:
                response = register_handler(request)
            elif "/login" in request:
                response = login_handler(request, address)
            elif "/logout" in request:
                response = logout_handler(request)
            elif "/add_product" in request:
                response = insert_product_handler(request)
            elif "/remove_product" in request:
                response = remove_product_handler(request, address)
            elif "/update_product" in request:
                response = update_product_handler(request, address)
            elif "/buy_product" in request:
                response = buy_product_handler(request)
            elif "/view_all_products" in request:
                response = view_all_products_handler()
            elif "/view_buyers" in request:
                response = view_buyers_handler(request)
            if response:
                add_cors_headers(response)
                client_socket.sendall(response.build_response().encode())
    except Exception as e:
        print(f"[SERVER] Error: {e}")
    finally:
        client_socket.close()


def start_server():
    """Starts the server."""
    conn = connect_to_database()
    create_tables(conn)
    conn.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind(("127.0.0.1", 30000))
    server_socket.listen(100)
    print("[SERVER] Listening on port 30000")

    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()


if __name__ == "__main__":
    start_server()
