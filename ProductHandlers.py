from Database import *
from request import *
from response import *
from product import *
from user import *
from Authentication import *
import json

def insert_product_handler(request):
    """Handles adding a product."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        username = body.get("username")
        name = body.get("name")
        picture = body.get("picture")
        price = body.get("price")
        description = body.get("description")
        quantity = body.get("quantity")

        if not all([username, name, picture, price, description, quantity]):
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Missing required fields"}))
            return response

        if insertProducts(username, name, picture, price, description,quantity, conn):
            response.set_status_code(201)
            response.set_body(json.dumps({"message": "Product added successfully"}))
        else:
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Failed to add product"}))
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid JSON format"}))
    except Exception as e:
        print(f"[SERVER] Error in insert_product_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()
    return response

def remove_product_handler(request, client_address):
    """Handles removing a product with validation."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        username = body.get("username")
        name = body.get("name")

        if not all([username, name]):
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Missing required fields"}))
            return response

        if removeProducts(username, name, conn, client_address, online_users):
            response.set_status_code(200)
            response.set_body(json.dumps({"message": "Product removed successfully"}))
        else:
            response.set_status_code(403)  
            response.set_body(json.dumps({"message": "Unauthorized or product not found"}))
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid JSON format"}))
    except Exception as e:
        print(f"[SERVER] Error in remove_product_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()
    return response


def update_product_handler(request, client_address):
    """Handles updating a product with validation."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        username = body.get("username")
        name = body.get("name")
        picture = body.get("picture")
        price = body.get("price")
        description = body.get("description")
        quantity = body.get("quantity")

        if not all([username, name, picture, price, description, quantity]):
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Missing required fields"}))
            return response

        if updateProducts(username, name, picture, price, description, quantity, conn, client_address, online_users):
            response.set_status_code(200)
            response.set_body(json.dumps({"message": "Product updated successfully"}))
        else:
            response.set_status_code(403)  
            response.set_body(json.dumps({"message": "Unauthorized or product not found"}))
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid JSON format"}))
    except Exception as e:
        print(f"[SERVER] Error in update_product_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()
    return response


def buy_product_handler(request):
    """
    Handles the purchase of a product. Handles both quantity decrement and product deletion.

    :param request: incoming HTTP request
    :type request: str
    :return: HTTP response
    :rtype: HttpResponse
    """
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")

    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        product_name = body.get("product_name")
        buyer_username = body.get("buyer_username")
        quantity_to_buy = body.get("quantity_to_buy")

        if not all([product_name, buyer_username, quantity_to_buy]):
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Missing required fields"}))
            return response

        quantity_to_buy = int(quantity_to_buy)

        if buyProducts(product_name, buyer_username, quantity_to_buy, conn, online_users):
            response.set_status_code(200)
            response.set_body(json.dumps({"message": "Product purchased successfully"}))
        else:
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Failed to purchase product"}))
    except ValueError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid quantity format"}))
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid JSON format"}))
    except Exception as e:
        print(f"[SERVER] Error in buy_product_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()

    return response



def view_all_products_handler():
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        products = getAllProducts(conn)
        if products:
            product_list = [
                {
                    "username": p[0],
                    "name": p[1],
                    "picture": p[2],
                    "price": p[3],
                    "description": p[4],
                    "quantity": p[5],  
                }
                for p in products
            ]
            response.set_status_code(200)
            response.set_body(json.dumps({"products": product_list}))
        else:
            response.set_status_code(200)
            response.set_body(json.dumps({"products": []}))
    except sqlite3.Error as e:
        print(f"[SERVER] Error in view_all_products_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()
    return response

