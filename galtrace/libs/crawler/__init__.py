#-*- coding: utf-8 -*-

import urllib.parse

from . import sites

UnsupportedLinkError = sites._UnsupportedLinkError

def fetch(uri):
    uri_ = urllib.parse.urlsplit(uri)
    return max(sites.factory, key=lambda x: x[0](uri_))[1](uri_)

__all__ = ['fetch', 'UnsupportedLinkError']
