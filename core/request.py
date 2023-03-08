import socket
import ssl

from .utils import schemes
from .utils.parser import show_content, parse
from .utils.handlers import RequestHandler, ResponseHandler
from .utils.constants import CONSTANTS

class Request:
    def __init__(self, url):
        self._url = url
        self._request = RequestHandler(self._url)

    def _connect_socket(self):
        schemes.set_scheme(self._url)
        self._host, self._port, self._path = self._request.handle_url()
        self._socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        if self._port != CONSTANTS.FILE_SCHEME_PORT:
            if CONSTANTS.SCHEME_IS_HTTPS:
                ctx = ssl.create_default_context()
                self._socket = ctx.wrap_socket(self._s, server_hostname=self._host)
            self._socket.connect((self._host, self._port))
            return True
        else:
            return False

    def _make_get_request(self):
        if not self._connect_socket() and self._port != CONSTANTS.FILE_SCHEME_PORT:
            print("[!] Something went wrong while creating a socket.")

        elif self._port == CONSTANTS.FILE_SCHEME_PORT:
            self._handle_response()
            return ''

        else:
            resp_header = f"GET {self._path} HTTP/1.1\r\n".encode("utf8")
            resp_header += f"Host: {self._host}\r\n\r\n".encode("utf8")
            resp_header += "Connection: close\r\n".encode("utf8")
            resp_header += f"User-Agent: {CONSTANTS.USER_AGENT}".encode("utf8")

            self._socket.send(resp_header)

            self._response = self._socket.makefile("r", encoding="utf8", newline="\r\n")
            return self._response

    def _handle_file_scheme(self):
        with open(self._host, 'r') as f:
            content = f.read()
            f.close()
        return "FILE", content

    def _handle_response(self):
        if self._port == CONSTANTS.FILE_SCHEME_PORT:
            headers, body = self._handle_file_scheme()

        else:
            response_handler = ResponseHandler(self._response)
            status_code = response_handler.get_status_code()
            assert status_code == "200", f"HTTP status code: {status_code}"
            headers, body = response_handler.get_headers_and_body()

        return headers, body

    def make(self):
        self._connect_socket()
        self._make_get_request()
        headers, body = self._handle_response()
        return headers, body


def load(url) -> None:
    if url == '': url = 'file:///Users/s/Desktop/Projects/engines/browser/default.html'
    headers, body = Request(url).make()
    cnt = parse(body)
    show_content(cnt, 'body')
