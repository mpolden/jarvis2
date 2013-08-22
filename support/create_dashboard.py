#!/usr/bin/env python

from __future__ import print_function
import os
import sys
from shutil import copyfile


class DashboardFactory(object):

    def __init__(self, name):
        self.name = name

    def create_dashboard(self):
        layout = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'app', 'templates', 'layouts',
            '{0}.html'.format(self.name)))
        if os.path.isfile(layout):
            print('{0} already exists'.format(layout))
            sys.exit(1)

        layout_template = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'templates', 'layout_empty.html'))
        copyfile(layout_template, layout)
        print(('Created {0}\nYour dashboard will be available at '
               '/dashboard/{1}').format(layout, self.name))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = raw_input('Name of the dashboard to create: ').lower()
    DashboardFactory(name).create_dashboard()
