import sys

def unsupported_url_scheme(scheme: str):
    print(f"UnsupportedUrlSchemeException: Does not support {scheme} type.")
    sys.exit(1)
