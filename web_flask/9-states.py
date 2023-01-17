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


@app.route('/states')
def list_states_view():
    """
    Returns the list of states present in the database
    by passing the states list into the template
    and also listing there cities.
    """
    s = storage.all(State).values()
    return render_template('9-states.html', states=s)


@app.route('/states/<id>')
def detail_state_view(id):
    """
    Returns details about states with id of `id`
    else return a 404 not found page
    """
    states = storage.all(State).values()
    state_info = None
    not_found = False
    for state in states:
        if state.id == id:
            state_info = state
            break
    if state_info is None:
        not_found = True
    state = {"state": state_info, "not_found": not_found}
    return render_template('9-detail_states.html', state=state) 


@app.teardown_appcontext
def teardown_context(exception):
    """
    closes the scoped session and reloads
    the session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
