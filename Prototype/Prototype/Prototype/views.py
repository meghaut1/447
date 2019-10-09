"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, g
from Prototype import app
import sqlite3

DATABASE = 'callCenter.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# run ipconfig in terminal then use the IPv4 address:5000 to access page
@app.route('/')
@app.route('/callCenter')
def callCenter():
    db = get_db() # test to connect to database. Error if it doesn't
    return render_template("callCenter.html")

@app.route('/incidentPanel')
def incidentPanel():
    return render_template('IncidentPanel.html')

