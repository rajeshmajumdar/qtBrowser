import curses

from core import request
from .draw import draw
from core.utils.constants import CONSTANTS


def load_url(url, window):
    content = request.load(url)
    for cnt in content:
        if cnt.type() == CONSTANTS.TEXT_OBJECT_TYPE:
            try:
                draw(window, cnt.get_str())
            except curses.error:
                pass


def load_text(text, window):
    draw(window, text)
