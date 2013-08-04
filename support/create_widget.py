#!/usr/bin/env python

from __future__ import print_function
import os
import sys
from jinja2 import Environment, FileSystemLoader


class WidgetFactory(object):

    def __init__(self, name):
        self.app_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     '..', 'app'))

        template_path = os.path.join(self.app_path, 'templates', 'widget')
        self.env = Environment(loader=FileSystemLoader(template_path),
                               keep_trailing_newline=True)
        self.name = name

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

    def create_widget(self):
        contents = self._render_templates()
        widget_dir = os.path.join(self.app_path, 'static', 'widgets',
                                  self.name)
        job_file = os.path.join(self.app_path, 'jobs', '%s.py' % (self.name,))

        if os.path.isdir(widget_dir):
            print('%s already exists' % (widget_dir,))
            sys.exit(1)
        if os.path.isfile(job_file):
            print('%s already exists' % (job_file,))
            sys.exit(1)

        os.mkdir(widget_dir)
        for filename in contents:
            if filename.endswith('.py'):
                file_path = job_file
            else:
                file_path = os.path.join(widget_dir, filename)
            with open(file_path, 'w') as f:
                f.write(contents[filename])
                print('Created %s' % (file_path,))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = raw_input('Name of the widget to create: ')
    WidgetFactory(name).create_widget()
