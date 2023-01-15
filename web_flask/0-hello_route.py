"""
A simple flask application that listens
on port 5000 and returns '/' route
"""

from flask import Flask
app = Flask(__name__.split('.')[0])


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run()
