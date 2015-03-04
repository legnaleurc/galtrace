import urllib.parse

from .sites import factory


def fetch(uri):
    uri = urllib.parse.urlsplit(uri)
    handler = max(factory, key=lambda x: x.evaluate(uri))
    return handler.parse(uri)
