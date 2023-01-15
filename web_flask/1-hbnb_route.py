#!/usr/bin/python3
"""
A simple flask application that listens
on port 5000 and returns '/' and '/hbnb'
routes
"""

from flask import Flask
app = Flask(__name__.split('.')[0])
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """
    A function that returns an the default
    route
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """
    The function displays HBNB! when the
    /hbnb route is hit
    """
    return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
