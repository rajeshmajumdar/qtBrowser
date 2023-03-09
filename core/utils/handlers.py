from io import BytesIO
from .constants import CONSTANTS


class RequestHandler:
    def __init__(self, url: str):
        self._url = url

    def _get_host_and_path(self, url: str):
        host, path = self._url.split('/', 1)
        path = '/' + path
        self._port = 443
        if ":" in host:
            host, port = host.split(':', 1)
            self._port = int(port)
        self._port = self._port if CONSTANTS.SCHEME_IS_HTTPS else 80
        return host, path

    def _handle_http(self):
        self._url = self._url[len('http://'):]
        host, path = self._get_host_and_path(self._url)
        return host, path

    def _handle_https(self):
        self._url = self._url[len('https://'):]
        host, path = self._get_host_and_path(self._url)
        return host, path

    def _handle_view_source(self):
        self._url = self._url[len('view-source:'):]
        if CONSTANTS.SCHEME_IS_HTTP:
            host, path = self._handle_http()
        elif CONSTANTS.SCHEME_IS_HTTPS:
            host, path = self._handle_https()
        else:
            unsupported_url_scheme(scheme)
        return host, path

    def _handle_file(self):
        filepath = self._url[len('file://'):]
        return filepath, 0

    def handle_url(self):
        if CONSTANTS.SCHEME_IS_HTTPS and not CONSTANTS.SCHEME_IS_VIEW_SOURCE:
            host, path = self._handle_https()
            return host, self._port, path
        elif CONSTANTS.SCHEME_IS_HTTP and not CONSTANTS.SCHEME_IS_VIEW_SOURCE:
            host, path = self._handle_http()
            return host, self._port, path
        elif CONSTANTS.SCHEME_IS_FILE and not CONSTANTS.SCHEME_IS_VIEW_SOURCE:
            host, path = self._handle_file()
            return host, CONSTANTS.FILE_SCHEME_PORT, path
        elif CONSTANTS.SCHEME_IS_VIEW_SOURCE:
            host, path = self._handle_view_source()
            return host, self._port, path

class ResponseHandler:
    def __init__(self, response):
        self._response = response

    def get_status_code(self):
        statusline = (self._response.readline()).decode("utf8")
        version, status, explaination = statusline.split(" ", 2)
        return status

    def _set_content_encoding(self, headers):
        if 'content-encoding' in headers:
            if headers['content_encoding'] == 'gzip':
                CONSTANTS.CONTENT_ENCODED_GZIP = True
        else:
            pass

    def _handle_chunked_transfer(self, headers, body):
        content = ''
        if 'transfer-encoding' in headers:
            if headers['transfer-encoding'] == 'chunked':
                body = BytesIO(body)
                while True:
                    line = body.readline().strip()
                    content_length = int(line, 16)

                    if content_length != 0:
                        content += body.read(content_length).decode("utf8")
                        content += "\r\n"
                    body.readline()

                    if content_length == 0:
                        break
                return content
        else:
            return body

    def get_headers_and_body(self):
        headers = {}
        while True:
            line = (self._response.readline()).decode("utf8")
            if line == "\r\n": break
            header, value = line.split(":", 1)
            headers[header.lower()] = value.strip()

        self._set_content_encoding(headers)
        body = self._response.read()
        body = self._handle_chunked_transfer(headers, body)

        return headers, body
