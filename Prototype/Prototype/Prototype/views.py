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
        g._database.close()
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
    print(name)
    # variables that need fields in the html
    city = 'Balimore'
    state = 'MD'
    zipCode = '21250'

    time = str(datetime.now()) # current date and time of submission

    conn = sqlite3.connect("callCenter.db")
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
    # need way to enter operator info
    #cur.execute('''INSERT INTO CallOperator (operID, name) VALUES (1001, 'Jane Doe')''')

    # adding taken value from html into the db
    # format input can do on Tuesday
    cur.execute('''INSERT INTO Victim (name, address, city, state, zipCode, phone) VALUES (?, ?, ?, ?, ?, ?)''', (name, address, city, state, zipCode, phoneNumber))
    row = cur.execute('''SELECT * FROM Victim''')
    print(row.fetchall())
    #row = cur.fetchall()
    #print(row)
    conn.commit()  
    cur.close()
    conn.close()
    return callCenter()

@app.route('/incidentPanel')
def incidentPanel():
    return render_template('IncidentPanel.html')
