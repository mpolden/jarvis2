#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys

try:
    # Python 2
    input = raw_input
except NameError:
    pass
from jinja2 import Environment, FileSystemLoader


class WidgetFactory(object):

    def __init__(self, name):
        self.name = name.lower()
        self.app_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     '..', 'app'))
        self.widget_dir = os.path.join(self.app_path, 'static', 'widgets',
                                       self.name)
        self.job_file = os.path.join(self.app_path, 'jobs',
                                     '%s.py' % (self.name,))
        template_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'templates', 'widget'))
        self.env = Environment(loader=FileSystemLoader(template_path),
                               keep_trailing_newline=True)

    def _render_templates(self):
        js = self.env.get_template('widget.js').render(name=self.name)
        css = self.env.get_template('widget.css').render(name=self.name)
        job = self.env.get_template('job.py').render(name=self.name)

        return {
            '%s.js' % (self.name,): js,
            '%s.css' % (self.name,): css,
            '%s.py' % (self.name,): job
        }

    def _create_widget_dir(self):
        os.mkdir(self.widget_dir)
        print('Created {}'.format(self.widget_dir))

    def _write_file(self, file_path, contents):
        with open(file_path, 'w') as f:
            f.write(contents)
            print('Created {}'.format(file_path))

    def create_widget(self):
        contents = self._render_templates()

        if os.path.isdir(self.widget_dir):
            print('%s already exists' % (self.widget_dir,))
            sys.exit(1)
        if os.path.isfile(self.job_file):
            print('%s already exists' % (self.job_file,))
            sys.exit(1)

        self._create_widget_dir()
        for filename in contents:
            if filename.endswith('.py'):
                file_path = self.job_file
            else:
                file_path = os.path.join(self.widget_dir, filename)
            self._write_file(file_path, contents[filename])

    def _remove_file(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            os.rmdir(file_path)
        print('Removed {}'.format(file_path))

    def remove_widget(self):
        if os.path.isdir(self.widget_dir):
            filenames = map(lambda f, e: f + e, (self.name,) * 2,
                            ('.js', '.css'))
            pyc_file = self.job_file + 'c'
            filenames += [self.job_file, pyc_file, self.widget_dir]
            for filename in filenames:
                file_path = os.path.join(self.widget_dir, filename)
                if not os.path.exists(file_path):
                    continue
                self._remove_file(file_path)

    def list_widgets(self):
        if not os.path.isdir(self.widget_dir):
            print('No such directory: {}'.format(self.widget_dir))
            sys.exit(1)

        for d in os.listdir(self.widget_dir):
            widget_path = os.path.join(self.widget_dir, d)
            name, _ = os.path.splitext(os.path.basename(d))
            print('{} {}'.format(name, widget_path))


class DryrunFactory(WidgetFactory):

    def _create_widget_dir(self):
        print('Would create {}'.format(self.widget_dir))

    def _write_file(self, file_path, contents):
        print('Would create {}'.format(file_path))

    def _remove_file(self, file_path):
        print('Would remove {}'.format(file_path))


def get_factory(name, dry_run=False):
    return DryrunFactory(name) if dry_run else WidgetFactory(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new widget.')
    parser.add_argument('-n', '--dry-run', dest='dry_run', action='store_true',
                        help=('Show what would be done, but don\'t'
                              ' do anything'))
    parser.add_argument('-l', '--list', dest='list_widgets',
                        action='store_true', help='List widgets')
    parser.add_argument('-r', '--remove', dest='remove', action='store_true',
                        help='Remove widget')
    parser.add_argument('name', metavar='NAME', nargs='?')
    args = parser.parse_args()

    if args.list_widgets:
        get_factory('', True).list_widgets()
    elif args.remove:
        name = args.name or input('Name of the widget to remove: ')
        get_factory(name, args.dry_run).remove_widget()
    else:
        name = args.name or input('Name of the widget to create: ')
        get_factory(name, args.dry_run).create_widget()
