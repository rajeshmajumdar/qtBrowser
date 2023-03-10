from ui.terminal import Terminal

if __name__ == "__main__":
    import sys
    try:
        url = sys.argv[1]
    except IndexError:
        url = ''

    Terminal().start(url)
