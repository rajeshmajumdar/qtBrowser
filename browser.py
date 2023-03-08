from core.request import load

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        load('')
    else:
        load(sys.argv[1])
