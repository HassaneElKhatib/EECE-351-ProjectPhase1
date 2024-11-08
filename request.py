class HttpRequest:
    def __init__(self, method="GET", url="/", host="localhost", headers=None, body=""):
        self.method = method
        self.url = url
        self.host = host
        self.headers = headers if headers is not None else {}
        self.body = body
        self.headers["Host"] = self.host

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body
        self.headers["Content-Length"] = str(len(self.body))

    @staticmethod
    def parse_http_request(request) -> dict:
        """
        Returns the method, uri, headers, content-type and body of an HTTP request.

        :param request: HTTP Request
        :type request: str
        :return: Dictionary containing the method, uri, headers, content-type and body of an HTTP request.
        :rtype: dict
        """
        try:
            lines = request.splitlines()
            request_line = lines[0]
            method, uri, _ = request_line.split(" ", 2)
            headers = {}
            i = 1
            while lines[i] != "":
                header_line = lines[i]
                header_key, header_value = header_line.split(": ", 1)
                headers[header_key] = header_value
                i += 1
            body = "\n".join(lines[i+1:])
            content_type = headers.get("Content-Type", "text/plain")

            return {
                "method": method,
                "uri": uri,
                "headers": headers,
                "content_type": content_type,
                "body": body
            }
        except Exception as e:
            print(f"Error parsing request: {e}")
            return None

    def build_request(self):
        """
        Constructs the HTTP request 

        :return: request
        :rtype: HTTPRequest
        """
        request = f"{self.method} {self.url} HTTP/1.1\r\n"
        for key, value in self.headers.items():
            request += f"{key}: {value}\r\n"
        request += "\r\n"
        request += self.body
        return request
