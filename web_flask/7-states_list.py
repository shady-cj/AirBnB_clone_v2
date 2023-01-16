#!/usr/bin/python3
"""
Flask application that fetches data from a database and
display its data using a template
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__.split('.')[0])

app.url_map.strict_slashes = False


@app.route('/states_list')
def list_states():
    s = storage.all(State).values()
    return render_template('7-states_list.html', states=s)


@app.teardown_appcontext
def teardown_context(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
