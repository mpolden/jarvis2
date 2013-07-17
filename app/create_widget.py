#!/usr/bin/env python

import os
import sys
from jinja2 import Environment, FileSystemLoader


class WidgetFactory(object):

    def __init__(self, name):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'templates', 'widget'))
        self.env = Environment(loader=FileSystemLoader(path))
        self.name = name

    def _render_templates(self):
        js = self.env.get_template('widget.js').render(name=self.name)
        less = self.env.get_template('widget.less').render(name=self.name)
        html = self.env.get_template('widget.html').render(name=self.name)

        return {
            '%s.js' % (self.name,): js,
            '%s.less' % (self.name,): less,
            '%s.html' % (self.name,): html
        }

    def create_widget(self):
        contents = self._render_templates()
        widget_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  'static', 'widgets',
                                                  self.name))
        if os.path.isdir(widget_dir):
            print '%s already exists' % (widget_dir,)
            sys.exit(1)
        os.mkdir(widget_dir)

        for filename in contents:
            widget_file = os.path.join(widget_dir, filename)
            with open(widget_file, 'w') as f:
                f.write(contents[filename])
                print 'Created %s' % (widget_file,)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = raw_input('Name of the widget to create: ')
    WidgetFactory(name).create_widget()
