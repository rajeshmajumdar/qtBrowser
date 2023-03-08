import socket
import ssl
import sys
from typing import Dict

from parser import show_content, parse

def handle_file(url: str) -> None:
    filepath: str = url[len('file://'):]
    with open(filepath, 'r') as f:
        content = f.read()
        f.close()
    cnt = parse(content)
    show_content(cnt['body'])
    sys.exit(1)

def request(url: str) -> (Dict, str):
    is_https: bool = False

    if url.startswith('https://'):
        is_https = True
    elif url.startswith('http://'):
        is_https = False
    elif url.startswith('file://'):
        handle_file(url)
    else:
        print('[!] Only supports http:// and https:// scheme.')

    url = url[len('https://'):] if is_https else url[len('http://')]
    host, path = url.split('/', 1)
    path: str = '/' + path

    port: int = 443
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    port = port if is_https else 80

    s = socket.socket(
        family = socket.AF_INET,
        type = socket.SOCK_STREAM,
        proto = socket.IPPROTO_TCP,
    )
    if is_https:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)
    s.connect((host, port))

    response_header = f"GET {path} HTTP/1.1\r\n".encode("utf8")
    response_header += f"Host: {host}\r\n\r\n".encode("utf8")
    response_header += f"Connection: close\r\n".encode("utf8")
    response_header += f"User-Agent: qtBrowser/0.6.9".encode("utf8")
    s.send(response_header)

    response = s.makefile("r", encoding="utf8", newline="\r\n")

    statusline = response.readline()
    version, status, explaination = statusline.split(" ", 2)
    assert status == "200", f"{status}: {explaination}"

    headers: Dict = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    assert "transfer-encoding" not in headers, "Currently it doesn't support any encoding"
    assert "content-encoding" not in headers, "Currently it doesn't support any encoding"

    body: str = response.read()
    s.close()

    return headers, body

def load(url) -> None:
    if url == '': url = 'file:///Users/s/Desktop/Projects/engines/browser/default.html'
    headers, body = request(url)
    cnt = parse(body)
    show_content(cnt['body'])
