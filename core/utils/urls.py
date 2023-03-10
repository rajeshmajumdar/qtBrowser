from .constants import CONSTANTS
from .errors import *
from .dev import DEBUG


def set_scheme(url):
    if url.startswith('http://'):
        CONSTANTS.SCHEME_IS_HTTP = True
    elif url.startswith('https://'):
        CONSTANTS.SCHEME_IS_HTTPS = True
    elif url.startswith('file://'):
        CONSTANTS.SCHEME_IS_FILE = True
    elif url.startswith('view-source:https://'):
        CONSTANTS.SCHEME_IS_VIEW_SOURCE = True
        CONSTANTS.SCHEME_IS_HTTPS = True
    elif url.startswith('view-source:http://'):
        CONSTANTS.SCHEME_IS_VIEW_SOURCE = True
        CONSTANTS.SCHEME_IS_HTTP = True
    elif url.startswith('/'):
        CONSTANTS.SCHEME_IS_PATH = True


def does_have_scheme():
    if CONSTANTS.SCHEME_IS_HTTP:
        return True
    if CONSTANTS.SCHEME_IS_FILE:
        return True
    if CONSTANTS.SCHEME_IS_HTTPS:
        return True
    if CONSTANTS.SCHEME_IS_VIEW_SOURCE:
        return True
    return False


def is_search_term(url):
    url = url.split(' ')
    return False if len(url) == 1 else True


def clean_url(url):
    if not url.endswith('/'):
        url = url + '/'

    if not does_have_scheme():
        if not is_search_term(url):
            CONSTANTS.SCHEME_IS_HTTP = True
            url = 'http://' + url

    return url

'''
google.com
https://google.com/
https://google.com
http://google.com/
http://google.com
google.com/some_path
google.com/some_path/

or just some random search term
'''
'''
if no_scheme:
    if not_search_term:
        add_http_scheme(url)

'''


def reset_schemes():
    CONSTANTS.SCHEME_IS_HTTP = False
    CONSTANTS.SCHEME_IS_HTTPS = False
    CONSTANTS.SCHEME_IS_FILE = False
    CONSTANTS.SCHEME_IS_VIEW_SOURCE = False
    CONSTANTS.SCHEME_IS_PATH = False
