#!/usr/bin/env python

import sys
import os
from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route('/')
def index():
    """Render index template"""
    return render_template('index.html')


@app.route('/styles.css')
def css():
    """Render widget styles"""
    response = make_response(render_template('styles.css'))
    response.headers['Content-Type'] = 'text/css'
    return response


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
