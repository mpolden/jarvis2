#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from shutil import copyfile


class DashboardFactory(object):

    def __init__(self, name, app_root=None, quiet=False):
        self.name = name
        self.quiet = quiet
        if app_root is None:
            app_root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '..'))
        self.layout_dir = os.path.join(app_root, 'templates', 'layouts')
        self.layout = os.path.join(self.layout_dir,
                                   '{0}.html'.format(self.name))

    def _print(self, s):
        if not self.quiet:
            print(s)

    def _write_file(self, file_path):
        layout_template = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'templates', 'layout_empty.html.j2'))
        copyfile(layout_template, file_path)
        self._print('Created {}'.format(file_path))

    def _remove_file(self, file_path):
        os.remove(file_path)
        self._print('Removed {}'.format(file_path))

    def create_dashboard(self):
        if os.path.isfile(self.layout):
            print('{} already exists'.format(self.layout))
            sys.exit(1)

        if not os.path.isdir(self.layout_dir):
            os.mkdir(self.layout_dir)
            self._print('Created {}'.format(self.layout_dir))

        self._write_file(self.layout)

        self._print('Your dashboard will be available at /dashboard/{}'.format(
            self.name))

    def remove_dashboard(self):
        if os.path.isfile(self.layout):
            self._remove_file(self.layout)

    def list_dashboards(self):
        if not os.path.isdir(self.layout_dir):
            print('No such directory: {}'.format(self.layout_dir))
            sys.exit(1)

        for d in os.listdir(self.layout_dir):
            layout_path = os.path.join(self.layout_dir, d)
            name, _ = os.path.splitext(os.path.basename(d))
            print('{} {}'.format(name, layout_path))


class DryrunFactory(DashboardFactory):

    def _create_dir(self):
        print('Would create {}'.format(self.dashboard_dir))

    def _write_file(self, file_path):
        print('Would create {}'.format(file_path))

    def _remove_file(self, file_path):
        print('Would remove {}'.format(file_path))


def get_factory(name, dry_run=False):
    return DryrunFactory(name) if dry_run else DashboardFactory(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new dashboard.')
    parser.add_argument('-n', '--dry-run', dest='dry_run', action='store_true',
                        help=('Show what would be done, but don\'t'
                              ' do anything'))
    parser.add_argument('-l', '--list', dest='list_dashboards',
                        action='store_true', help='List dashboards')
    parser.add_argument('-r', '--remove', dest='remove', action='store_true',
                        help='Remove dashboard')
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()

    if args.list_dashboards:
        get_factory('', True).list_dashboards()
    elif args.remove:
        name = args.name or input('Name of the dashboard to remove: ')
        get_factory(name, args.dry_run).remove_dashboard()
    else:
        name = args.name or input('Name of the dashboard to create: ')
        get_factory(name, args.dry_run).create_dashboard()
