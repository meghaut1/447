"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, g, request
from Prototype import app
import sqlite3

DATABASE = 'callCenter.db'
CALLID = 1000

def getCallID():
  global CALLID
  CALLID = CALLID + 1
  return CALLID

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
    name = request.form['name']
    urgency = request.form['Urgency']
    time = str(datetime.now()) # current date and time of submission
    conn = get_db()
    cur = conn.cursor()
    '''
    Table entry order
    1) Operator
    2) Victim
    3) Call
    4) Event
    5) Mission
    '''
    # Operator
    #cur.execute("INSERT INTO CallOperator (operID, name) VALUES ('1001', 'Jane Doe')")

    res = cur.execute("SELECT * FROM Call")
    print(res)
    cur.close()
    conn.close()
    return callCenter()

@app.route('/incidentPanel')
def incidentPanel():
    return render_template('IncidentPanel.html')
