import importlib
import pkgutil
import sys


class UnsupportedLinkError(RuntimeError):
    pass


class UnavailableLinkError(RuntimeError):
    pass


class Site(object):

    def evaluate(self, uri):
        try:
            score = self.do_evaluate(uri)
        except Exception as e:
            raise UnavailableLinkError(e.message) from e
        return score

    def parse(self, uri):
        try:
            data = self.do_parse(uri)
        except UnsupportedLinkError:
            raise
        except Exception as e:
            raise UnavailableLinkError(e.message) from e
        return data

    def do_evaluate(self, uri):
        return 1

    def do_parse(self, uri):
        raise UnsupportedLinkError('unsupported link')


def package_walker(package_name):
    path = sys.modules[package_name].__path__
    for module_finder, name, ispkg in pkgutil.walk_packages(path):
        if ispkg:
            continue
        module = importlib.import_module('.' + name, package_name)
        yield module


factory = [module.Site() for module in package_walker(__name__)]
factory.insert(0, Site())
