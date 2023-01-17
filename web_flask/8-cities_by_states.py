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


@app.route('/cities_by_states')
def list_states():
    """
    Returns the list of states present in the database
    by passing the states list into the template
    and also listing there cities.
    """
    s = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=s)


@app.teardown_appcontext
def teardown_context(exception):
    """
    closes the scoped session and reloads
    the session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
