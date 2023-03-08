from .constants import CONSTANTS
from .errors import *

def set_scheme(url):
    if url.startswith('http://'):
        CONSTANTS.SCHEME_IS_HTTP = True
    elif url.startswith('https://'):
        CONSTANTS.SCHEME_IS_HTTPS = True
    elif url.startswith('file://'):
        CONSTANTS.SCHEME_IS_FILE = True
    else:
        scheme = url.split(':')[0]
        scheme = scheme + "://"
        unknown_url_scheme(scheme)
