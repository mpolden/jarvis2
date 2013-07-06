#!/usr/bin/env python

import os
import sys
from jinja2 import Environment, FileSystemLoader


def render_templates(name):
    env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.join(
                                              os.path.dirname(__file__),
                                              'templates', 'widget'))))
    return {
        '%s.js' % (name,): env.get_template('widget.js').render(name=name),
        '%s.less' % (name,): env.get_template('widget.less').render(name=name),
        '%s.html' % (name,): env.get_template('widget.html').render(name=name),
    }


def create_widget(contents, name):
    widgets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               'static', 'widgets', name))
    if os.path.isdir(widgets_dir):
        print '%s already exists' % (widgets_dir,)
        sys.exit(1)

    os.mkdir(widgets_dir)

    for filename in contents:
        widget_dir = os.path.join(widgets_dir, filename)
        with open(widget_dir, 'w') as f:
            f.write(contents[filename])
            print 'Created %s' % (widget_dir,)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: %s name' % (sys.argv[0],)
        sys.exit(1)
    name = sys.argv[1]
    contents = render_templates(name)
    create_widget(contents, name)
