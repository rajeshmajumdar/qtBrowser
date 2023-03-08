import sys

def unknown_url_scheme(scheme: str):
    print(f"UnknownUrlSchemeException: Does not support {scheme} type.")
    sys.exit(1)
