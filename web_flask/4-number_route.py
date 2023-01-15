#!/usr/bin/python3
"""
A simple flask application that listens
on port 5000 and returns different
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


@app.route('/c/<text>')
def c_route(text):
    """
    The function returns the string
    C <text>(replacing all _ with ' ')
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_route(text):
    """
    python_route returns a string
    Python <text> where the default value
    of text is "is cool"
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def is_number(n):
    """
    A route that takes strictly a number
    """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
