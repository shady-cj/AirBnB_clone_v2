#!/usr/bin/python3
"""
Flask application that fetches data from a database and
display its data using a template
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__.split('.')[0])

app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def filters_list_detail_view():
    """
    Returns information about states, cities in states,
    amenities.
    """
    s = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=s, amenities=amenities)


@app.teardown_appcontext
def teardown_context(exception):
    """
    closes the scoped session and reloads
    the session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
