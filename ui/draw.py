import curses

def draw(window, content):
    window.addstr(content)
    window.refresh()
