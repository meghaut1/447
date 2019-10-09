"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, g, request
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
    db.close()
    return render_template("callCenter.html")

# gets input from HTML page
@app.route('/', methods=['POST'])
def getInfo():
    address = request.form['address']
    phoneNumber = request.form['phoneNumber']
    date = request.form['timestamp']
    urgency = request.form['Urgency']
    time = datetime.now() # current date and time of submission
    return callCenter()

@app.route('/incidentPanel')
def incidentPanel():
    return render_template('IncidentPanel.html')

