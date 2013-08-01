#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from importlib import import_module
from pkgutil import iter_modules
from os.path import dirname, basename


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


def load_jobs():
    return dict([(cls.__name__.lower(), cls) for cls in AbstractJob.load()])
