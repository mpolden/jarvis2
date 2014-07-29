#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from pkgutil import iter_modules
from os.path import dirname, basename

# import_module wasn't added until 2.7
try:
    from importlib import import_module
except ImportError:
    def import_module(name):
        __import__(name)


class AbstractJob(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        pass

    @classmethod
    def load(cls):
        paths = [dirname(__file__)]
        prefix = '%s.' % (basename(paths[0]),)
        for _, name, is_pkg in iter_modules(paths, prefix):
            if not is_pkg:
                import_module(name)
        return AbstractJob.__subclasses__()

    def __str__(self):
        return '[name={}, interval={}, timeout={}, start_date={}]'.format(
            self.__class__.__name__.lower(),
            getattr(self, 'interval', None),
            getattr(self, 'timeout', None),
            getattr(self, 'start_date', None))


def load_jobs():
    return dict([(cls.__name__.lower(), cls) for cls in AbstractJob.load()])
