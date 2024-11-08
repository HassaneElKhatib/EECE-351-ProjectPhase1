class HttpResponse:
    def __init__(self, status_code=200, headers=None, body=""):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.body = body

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body

    def set_status_code(self, code):
        self.status_code = code

    def build_response(self):
        status_message = self._get_status_message(self.status_code)
        response = f"HTTP/1.1 {self.status_code} {status_message}\r\n"
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"
        response += "\r\n"
        response += self.body
        return response

    @staticmethod
    def parse_http_response(response):
        """
        Parses HTTP response, and returns protocol, status code, status message, headers and body.

        :param response: HTTP response
        :type response: str
        :return: Dictionary containing the protocol, the status code, the status message, the headers and a body
        :rtype: dict
        """
        try:
            lines = response.splitlines()
            status_line = lines[0]
            protocol, status_code, status_message = status_line.split(" ", 2)
            headers = {}
            i = 1
            while lines[i] != "":
                header_line = lines[i]
                header_key, header_value = header_line.split(": ", 1)
                headers[header_key] = header_value
                i += 1
            body = "\n".join(lines[i+1:])
            return {
                "protocol": protocol,
                "status_code": int(status_code),
                "status_message": status_message,
                "headers": headers,
                "body": body
            }

        except Exception as e:
            print(f"Error parsing response: {e}")
            return None

    @staticmethod
    def _get_status_message(status_code):
        """
        Returns the status_message of the HTTP response

        :param status_code: response code
        :type status_code: string
        :return: response message
        :rtype: str
        """
        messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }
        return messages.get(status_code, "Unknown Status")
