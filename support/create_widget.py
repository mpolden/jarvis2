#!/usr/bin/env python

"""JARVIS 2 - create widget

Usage:
  create_widget.py [-l | [-r] [-n] [NAME]]

Options:
  -h --help         Show usage
  -n --dry-run      Show what would be done, but don't do anything
  -l --list         List widgets
  -r --remove       Remove widget

"""
from __future__ import print_function

import os
import sys

from clint.textui import colored, puts
from docopt import docopt
from jinja2 import Environment, FileSystemLoader


class WidgetFactory(object):

    def __init__(self, name):
        self.name = name
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
        less = self.env.get_template('widget.less').render(name=self.name)
        html = self.env.get_template('widget.html').render(name=self.name)
        job = self.env.get_template('job.py').render(name=self.name)

        return {
            '%s.js' % (self.name,): js,
            '%s.less' % (self.name,): less,
            '%s.html' % (self.name,): html,
            '%s.py' % (self.name,): job
        }

    def _create_widget_dir(self):
        os.mkdir(self.widget_dir)
        puts('Created %s' % (colored.green(self.widget_dir),))

    def _write_file(self, file_path, contents):
        with open(file_path, 'w') as f:
            f.write(contents)
            puts('Created %s' % (colored.green(file_path),))

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
        puts('Removed %s' % (colored.red(file_path),))

    def remove_widget(self):
        if os.path.isdir(self.widget_dir):
            filenames = map(lambda f, e: f + e, (self.name,) * 3,
                            ('.html', '.js', '.less'))
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


class UselessFactory(WidgetFactory):

    def _create_widget_dir(self):
        puts('Would create %s' % (colored.green(self.widget_dir),))

    def _write_file(self, file_path, contents):
        puts('Would create %s' % (colored.green(file_path),))

    def _remove_file(self, file_path):
        puts('Would remove %s' % (colored.red(file_path),))


def get_factory(name, dry_run=False):
    return UselessFactory(name) if dry_run else WidgetFactory(name)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['--list']:
        get_factory('', True).list_widgets()
    elif args['--remove']:
        name = args['NAME'] or raw_input('Name of the widget to remove: ')
        get_factory(name, args['--dry-run']).remove_widget()
    else:
        name = args['NAME'] or raw_input('Name of the widget to create: ')
        get_factory(name, args['--dry-run']).create_widget()
