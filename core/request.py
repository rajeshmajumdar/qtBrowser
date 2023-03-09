import socket
import ssl

from .utils import schemes
from .utils.parser import lex, parse, show_source
from .utils.handlers import RequestHandler, ResponseHandler
from .utils.constants import CONSTANTS

from .utils.dev import DEBUG


class Request:
    def __init__(self, url):
        self._url = url
        self._request = RequestHandler(self._url)

    def _connect_socket(self):
        schemes.set_scheme(self._url)
        self._host, self._port, self._path = self._request.handle_url()
        DEBUG(f"{self._host} - {self._path}")
        self._socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        if self._port != CONSTANTS.FILE_SCHEME_PORT:
            if CONSTANTS.SCHEME_IS_HTTPS:
                ctx = ssl.create_default_context()
                self._socket = ctx.wrap_socket(
                    self._socket,
                    server_hostname=self._host)

            self._socket.connect((self._host, self._port))
            return True
        else:
            return False

    def _make_get_request(self, socket_status):
        if not socket_status and self._port != CONSTANTS.FILE_SCHEME_PORT:
            print("[!] Something went wrong while creating a socket.")

        elif self._port == CONSTANTS.FILE_SCHEME_PORT:
            self._handle_response()
            return ''

        else:
            resp_header = f"GET {self._path} HTTP/1.1\r\n".encode("utf8")
            resp_header += f"Host: {self._host}\r\n\r\n".encode("utf8")
            resp_header += "Connection: close\r\n".encode("utf8")
            resp_header += f"User-Agent: {CONSTANTS.USER_AGENT}".encode("utf8")
            resp_header += "Accept-Encoding: gzip".encode("utf8")

            self._socket.send(resp_header)

            self._response = self._socket.makefile("rb", newline="\r\n")
            return self._response

    def _handle_file_scheme(self):
        with open(self._host, 'r') as f:
            content = f.read()
            f.close()
        return "FILE", content

    def _handle_redirects(self, headers):
        schemes.reset_schemes()
        try:
            location = headers['location']
            schemes.set_scheme(location)
            if CONSTANTS.SCHEME_IS_PATH:
                location = self._host + location
                CONSTANTS.SCHEME_IS_PATH = False
            else:
                location = location

            DEBUG(location)
            headers, body = Request(location).make()
            return headers, body
        except KeyError:
            print('[!] Bad redirect response.')

        return headers, body

    def _handle_response(self):
        if self._port == CONSTANTS.FILE_SCHEME_PORT:
            headers, body = self._handle_file_scheme()

        else:
            response_handler = ResponseHandler(self._response)
            status_code = response_handler.get_status_code()
            headers, body = response_handler.get_headers_and_body()
            if status_code == "301":
                headers, body = self._handle_redirects(headers)

        return headers, body

    def make(self):
        DEBUG(self._url)
        socket_status = self._connect_socket()
        self._make_get_request(socket_status)
        headers, body = self._handle_response()
        self._socket.close()
        return headers, body


def load(url) -> None:
    if url == '':
        url = CONSTANTS.DEFAULT_HTML_FILE
    headers, body = Request(url).make()
    if CONSTANTS.SCHEME_IS_VIEW_SOURCE:
        show_source(body)
    else:
        cnt = parse(body)
        text = lex(cnt, 'body')
        return text
