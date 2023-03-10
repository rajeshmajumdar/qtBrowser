import re
from typing import Dict
from gzip import decompress

from .constants import CONSTANTS
from .text import Text, Tag

from .dev import DEBUG


# TODO: Currently just skipping the brackets, need a better implementation.
def lex(body: str, tag: str) -> str:
    output = []
    text = ""
    in_tags = False
    try:
        for c in body[tag]:
            if c == "<":
                in_tags = True
                if text:
                    output.append(Text(text))
                text = ""
            elif c == ">":
                in_tags = False
                output.append(Tag(text))
                text = ""
            else:
                text += c
        if not in_tags and text:
            output.append(Text(text))

        return output
    except Exception as e:
        print(e)

    DEBUG("Text starts here:\n" + text)

    return text


def handle_entities(body: str) -> str:
    entities = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&apos;': "'",
        '&cent;': '¢',
        '&pound;': '£',
        '&yen;': '¥',
        '&euro;': '€',
        '&copy;': '©',
        '&reg;': '®',
    }
    for entity in entities.keys():
       body = re.sub(entity, entities[entity], body)

    return body


def parse(body: str) -> Dict:
    try:
        body = body.decode("utf8")
    except AttributeError:
        pass

    if CONSTANTS.CONTENT_ENCODED_GZIP:
        body = decompress(body)

    content: Dict = {}
    body = handle_entities(body)
    title = re.search('<title[^>]*>((.|[\n\r])*)<\/title>', body)
    body = re.search('<body[^>]*>((.|[\n\r])*)<\/body>', body)
    content['title'] = title.group(0)
    content['body'] = body.group(0)
    return content


def show_source(body: str) -> None:
    body = re.sub('&lt;', '<', body)
    body = re.sub('&gt;', '>', body)
    print(body)
