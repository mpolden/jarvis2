#!/usr/bin/env python

"""JARVIS 2 - create dashboard

Usage:
  create_dashboard.py [-r] [-n] [NAME]

Options:
  -h --help         Show usage
  -n --dry-run      Show what would be done, but don't do anything
  -r --remove       Remove dashboard

"""
from __future__ import print_function

import os
import sys

from clint.textui import colored, puts
from docopt import docopt
from shutil import copyfile


class DashboardFactory(object):

    def __init__(self, name):
        self.name = name
        self.layout_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'app', 'templates', 'layouts'))
        self.layout = os.path.join(self.layout_dir,
                                   '{0}.html'.format(self.name))

    def _write_file(self, file_path):
        layout_template = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'templates', 'layout_empty.html'))
        copyfile(layout_template, file_path)
        puts('Created {}'.format(colored.green(file_path)))

    def _remove_file(self, file_path):
        os.remove(file_path)
        puts('Removed {}'.format(colored.red(file_path)))

    def create_dashboard(self):
        if os.path.isfile(self.layout):
            print('{} already exists'.format(self.layout))
            sys.exit(1)

        if not os.path.isdir(self.layout_dir):
            os.mkdir(self.layout_dir)
            print('Created {}'.format(colored.green(self.layout_dir)))

        self._write_file(self.layout)

        print('Your dashboard will be available at /dashboard/{}'.format(
            self.name))

    def remove_dashboard(self):
        if os.path.isfile(self.layout):
            self._remove_file(self.layout)


class DryrunFactory(DashboardFactory):

    def _create_dir(self):
        puts('Would create {}'.format(colored.green(self.dashboard_dir)))

    def _write_file(self, file_path):
        puts('Would create {}'.format(colored.green(file_path)))

    def _remove_file(self, file_path):
        puts('Would remove {}'.format(colored.red(file_path)))


def get_factory(name, dry_run=False):
    return DryrunFactory(name) if dry_run else DashboardFactory(name)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['--remove']:
        name = args['NAME'] or raw_input('Name of the dashboard to remove: ')
        get_factory(name, args['--dry-run']).remove_dashboard()
    else:
        name = args['NAME'] or raw_input('Name of the dashboard to create: ')
        get_factory(name, args['--dry-run']).create_dashboard()
