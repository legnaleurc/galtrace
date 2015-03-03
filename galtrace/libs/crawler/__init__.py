#-*- coding: utf-8 -*-

import urllib.parse
import urllib.error

from . import sites

UnsupportedLinkError = sites._UnsupportedLinkError

class UnavailableLinkError(RuntimeError):
    pass

def fetch(uri):
    uri = urllib.parse.urlsplit(uri)
    try:
        handler = max(sites.factory, key=lambda x: x[0](uri))
    except urllib.error.HTTPError as e:
        raise UnavailableLinkError(e.code)
    return handler[1](uri)

__all__ = ['fetch', 'UnsupportedLinkError', 'UnavailableLinkError']
