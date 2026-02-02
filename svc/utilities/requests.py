import json
from http.client import HTTPResponse
from urllib import request


class requests:

    @staticmethod
    def get(url, headers={}, stream=False, timeout=None):
        http_request = request.Request(url, headers=headers, method="GET")

        try:
            resp = request.urlopen(http_request, timeout=timeout)
            return Response(resp, stream=stream)

        except Exception as e:
            print(f"An error occurred: {e}")


class Response:
    def __init__(self, raw_content: HTTPResponse, stream=False):
        self.status_code = raw_content.status
        self._raw_content = raw_content
        self.stream = stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._raw_content:
            self._raw_content.close()


    def raise_for_status(self):
        error_message = ''
        if self.status_code >= 500:
            error_message = f"HTTP Server Error: {self.status_code}"
        elif self.status_code >= 400:
            error_message = f"HTTP Client Error: {self.status_code}"

        if error_message:
            raise Exception(error_message)

    def json(self):
        response = self._raw_content.read()
        content = response.decode('utf-8')
        return json.loads(content)

    def iter_content(self, chunk_size=8192):
        while True:
            chunk = self._raw_content.read(chunk_size)
            if not chunk:
                break
            yield chunk
