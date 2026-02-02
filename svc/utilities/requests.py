import json
from urllib import request


class requests:

    @staticmethod
    def get(url, headers={}, stream=False, timeout=None):
        http_request = request.Request(url, headers=headers, method="GET")

        try:
            with request.urlopen(http_request, timeout=timeout) as response:
                body_bytes = response.read()
                body_string = body_bytes.decode('utf-8')

                return Response(response.status, body_string)

        except Exception as e:
            print(f"An error occurred: {e}")


class Response:
    def __init__(self, status_code: int, content: str):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        error_message = ''
        if self.status_code >= 500:
            error_message = f"HTTP Server Error: {self.status_code}"
        elif self.status_code >= 400:
            error_message = f"HTTP Client Error: {self.status_code}"

        if error_message:
            raise Exception(error_message)

    def json(self):
        return json.loads(self.content)
