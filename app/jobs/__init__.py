#!/usr/bin/env python

import os.path
from abc import ABCMeta, abstractmethod
from imp import find_module, load_module
from pkgutil import iter_modules


class AbstractJob(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        pass

    @classmethod
    def load(cls):
        paths = [os.path.dirname(__file__)]
        for _, name, _ in iter_modules(paths):
            f, filename, fileinfo = find_module(name, paths)
            load_module(name, f, filename, fileinfo)
            f.close()
        return dict([(c.__name__.lower(), c) for c in
                     AbstractJob.__subclasses__()])
