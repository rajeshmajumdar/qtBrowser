from core.request import load

if __name__ == "__main__":
    import sys
    try:
        load(sys.argv[1])
    except KeyError:
        load('')
