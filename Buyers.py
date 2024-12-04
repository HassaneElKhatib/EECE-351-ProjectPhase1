from Database import *
from request import *
from response import *
from product import *
from user import *
import json

def view_buyers_handler(request):
    """Handles viewing buyers of a user's products."""
    response = HttpResponse()
    conn = sqlite3.connect("auboutique.db")
    try:
        body = json.loads(request.split("\r\n\r\n")[1])
        seller_username = body.get("username")

        if not seller_username:
            response.set_status_code(400)
            response.set_body(json.dumps({"message": "Missing seller username"}))
            return response

        buyers = viewBuyers(seller_username, conn)
        if buyers:
            response.set_status_code(200)
            response.set_body(json.dumps({"buyers": buyers}))
        else:
            response.set_status_code(404)
            response.set_body(json.dumps({"message": "No buyers found"}))
    except json.JSONDecodeError:
        response.set_status_code(400)
        response.set_body(json.dumps({"message": "Invalid JSON format"}))
    except Exception as e:
        print(f"[SERVER] Error in view_buyers_handler: {e}")
        response.set_status_code(500)
        response.set_body(json.dumps({"message": "Internal server error"}))
    finally:
        conn.close()
    return response
