import tkinter
from typing import List

from core import request
from core.utils.constants import CONSTANTS


class Browser:
    def __init__(self):
        self._window = tkinter.Tk()
        self._canvas = tkinter.Canvas(
            self._window,
            width=CONSTANTS.WINDOW_WIDTH,
            height=CONSTANTS.WINDOW_HEIGHT
        )
        self._canvas.pack()
        self._scroll = 0
        self._window.bind(
            "<Button-4>",
            self._scrollDown)

    def _scrollDown(self, e):
        self._scroll += CONSTANTS.SCROLL_STEP
        self._draw()

    def _layout(self, content) -> List:
        HSTEP, VSTEP = 13, 18
        cursor_x, cursor_y = HSTEP, VSTEP
        display_content = []
        for cnt in content:
            if cnt == '\n':
                cursor_y += VSTEP + 10
                cursor_x = HSTEP
            display_content.append((cursor_x, cursor_y, cnt))
            if cursor_x >= CONSTANTS.WINDOW_WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
            cursor_x += HSTEP
        return display_content

    def _draw(self):
        self._canvas.delete("all")
        VSTEP = 18
        for x, y, c in self._display_content:
            if y > self._scroll + CONSTANTS.WINDOW_HEIGHT:
                continue
            if y + VSTEP < self._scroll:
                continue
            self._canvas.create_text(x, y - self._scroll, text=c)

    def load(self, url):
        text = request.load(url)
        self._display_content = self._layout(text)
        self._draw()


if __name__ == "__main__":
    import sys
    try:
        url = sys.argv[1]
    except IndexError:
        url = ''

    #print(request.load(url))

    Browser().load(url)
    tkinter.mainloop()
