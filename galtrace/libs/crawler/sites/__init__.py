import pkgutil
import sys

from .base import UnsupportedLinkError
from .base import UnavailableLinkError


def package_walker(package_name):
    path = sys.modules[package_name].__path__
    for module_finder, name, ispkg in pkgutil.walk_packages(path):
        if ispkg:
            continue
        loader = module_finder.find_module(name)
        module = loader.load_module('{0}.{1}'.format(package_name, name))
        yield module


factory = [module.Site() for module in package_walker(__name__)]
