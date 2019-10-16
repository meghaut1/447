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
    # variables for the Operator
    operID = request.form['id']
    name = request.form['name']
    ######################

    # variables for the Victim
    vName = request.form['vName']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zipCode = request.form['zipCode']
    #city = 'Balimore'
    #state = 'MD'
    #zipCode = '21250'

    # variables for Call
    callID = getCallID()
    t = datetime.now()
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    # Use the above link if you would like to change the formatting of date or time

    date = t.strftime("%d/%m/%y") # strftime() returns a formatted string. Format of date is day/month/year. 
    time = t.strftime("%H:%M") # 24 hour time. Format of time is hours:minutes
    phoneNumber = request.form['phoneNumber']
    urgency = request.form['Urgency']
    emergency = request.form['emergency']

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

    extends = '{% extends "IncidentPanel.html" %}'
    block = '{% block table %}'
    endblock = '{% endblock %}'
	# create a main list.
    mainList = []

	# for each row in the database for the Call Center:
		# add each value in the row to a sublist. I.e., subList = [timestamp, type, address, phone, urgency]
		# append this sublist to the main list. I.e., mainList.append(subList)

	# for i in main list of data:
	#htmlString = "<tr class=\"data\">"
	#+ "<td>" + 'TIMESTAMP VARIABLE IN SUBLIST[i]'
	#+ "</td><td>" + 'TYPE VARIABLE IN SUBLIST[i]'
	#+ "</td><td>" + 'ADDRESS VARIABLE IN SUBLIST[i]'
	#+ "</td><td>" + 'PHONE VARIABLE IN SUBLIST[i]'
	#+ "</td><td>" + 'URGENCY VARIABLE IN SUBLIST[i]'
  #+ "</td></tr>"

	# append this htmlString to the HTML table.
    #htmlString = extends + block + htmlString + endblock
    #with open("Prototype/templates/IncidentTable.html", "w") as f
    #   f.write(htmlString)
    #return render_template('IncidentTable.html')
    return render_template('IncidentPanel.html')
