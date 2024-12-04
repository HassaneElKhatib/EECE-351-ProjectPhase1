from Database import *
from request import *
from response import *
from product import *
from user import *
import threading
import json

online_users = {}
online_users_lock = threading.Lock()

def register_handler(request):
    """Handles user registration."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        name = body.get("name")
        email = body.get("email")
        address = body.get("address")
        username = body.get("username")
        password = body.get("password")

        if not all([name, email, address, username, password]):
            response.set_status_code(400)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Missing required fields"})
            return response

        if register(name, email, address, username, password, conn):
            response.set_status_code(201)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Registration successful"})
        else:
            response.set_status_code(400)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Registration failed. User may already exist."})
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Invalid JSON format"})
    except Exception as e:
        print(f"[SERVER] Error in register_handler: {e}")
        response.set_status_code(500)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Internal server error"})
    finally:
        conn.close()
    return response


def login_handler(request, client_address):
    """Handles user login."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = request.split("\r\n\r\n", 1)[1]
        if not body.strip():
            raise ValueError("Empty request body")

        body = json.loads(body)
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            response.set_status_code(400)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Missing username or password"})
            return response

        client_ip = client_address[0]
        client_port = client_address[1]

        if login(username, password, conn):
            with online_users_lock:
                online_users[username] = {"ip": client_ip, "port": client_port}

            response.set_status_code(200)
            response.set_header("Content-Type", "application/json")
            response.set_body({
                "message": "Login successful",
                "ip": client_ip,
                "port": client_port,
                "username": username,
            })
        else:
            response.set_status_code(401)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Invalid username or password"})
    except ValueError as e:
        print(f"[SERVER] ValueError: {e}")
        response.set_status_code(400)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": str(e)})
    except json.JSONDecodeError as e:
        print(f"[SERVER] JSON Decode Error: {e}")
        response.set_status_code(400)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Invalid JSON format"})
    except Exception as e:
        print(f"[SERVER] Error in login_handler: {e}")
        response.set_status_code(500)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Internal server error"})
    finally:
        conn.close()
    return response



def logout_handler(request):
    """Handles user logout."""
    response = HttpResponse()
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        username = body.get("username")
        ip = body.get("ip")
        port = body.get("port")

        if not username or not ip or not port:
            response.set_status_code(400)
            response.set_header("Content-Type", "application/json")
            response.set_body({"message": "Missing username, IP, or port"})
            return response

        with online_users_lock:
            if username in online_users:
                del online_users[username]
                print(f"[DEBUG] User '{username}' logged out from IP {ip} and port {port}.")
            else:
                print(f"[DEBUG] User '{username}' not found in online_users.")

        response.set_status_code(200)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Logout successful"})
    except json.JSONDecodeError as e:
        response.set_status_code(400)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Invalid JSON format"})
        print(f"[SERVER] JSON Decode Error: {e}")
    except Exception as e:
        print(f"[SERVER] Error in logout_handler: {e}")
        response.set_status_code(500)
        response.set_header("Content-Type", "application/json")
        response.set_body({"message": "Internal server error"})
    return response
