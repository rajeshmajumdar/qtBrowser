import re
from typing import Dict

# TODO: Currently just skipping the brackets, need a better implementation.
def show_content(body: str, tag: str) -> None:
    in_angle = False
    try:
        for c in body[tag]:
            if c == "<":
                in_angle = True
            elif c == ">":
                in_angle = False
            elif not in_angle:
                print(c, end="")
    except Exception as e:
        print(e)

def parse(body: str) -> Dict:
    content: Dict = {}
    body = re.sub('&lt;', '<', body)
    body = re.sub('&gt;', '>', body)
    title = re.search('<title[^>]*>((.|[\n\r])*)<\/title>', body)
    body = re.search('<body[^>]*>((.|[\n\r])*)<\/body>', body)
    content['title'] = title.group(0)
    content['body'] = body.group(0)
    return content

def show_source(body: str) -> None:
    print(body)
