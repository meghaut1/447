"""
Routes and views for the flask application.
"""
# https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
# Use the above link if you would like to change the formatting of date or time
from datetime import datetime
from flask import render_template, g, request
from Prototype import app
import sqlite3

DATABASE = 'callCenter.db'
CALLID = 1000
EVENTID = 2000

# Generates new callID for Call table
def getCallID():
  global CALLID
  events = pullEvent()
  ids = [x[1] for x in events]
  while CALLID in ids:
        CALLID = CALLID + 4
  return CALLID

# Generates new eventID for Event table
def getEventID():
    global EVENTID
    events = pullEvent()
    ids = [x[0] for x in events]
    while EVENTID in ids:
        EVENTID += 1
    return EVENTID


# Test db connection
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
    print('here')

    # variables for the Operator
    operID = request.form['id']
    name = request.form['name']
    print(name + " " + operID)
    
    # variables for the Victim
    vName = request.form['vName']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zipCode = request.form['zipCode']

    # variables for Call
    t = datetime.now()
    date = t.strftime("%d/%m/%y") # strftime() returns a formatted string. Format of date is day/month/year.
    time = t.strftime("%H:%M") # 24 hour time. Format of time is hours:minutes (00:00 - 23:59)
    phoneNumber = request.form['phoneNumber']
    emergency = request.form['emergency']
    callID = getCallID()

    # variables for Event
    urgency = request.form['Urgency']
    eventID = getEventID()
    
    # Opening db
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()

    # Adding victim info
    cur.execute('''INSERT INTO Victim (name, address, city, state, zipCode, phone) VALUES (?, ?, ?, ?, ?, ?)''', (vName, address, city, state, zipCode, phoneNumber))
    # Adding operator info
    cur.execute('''INSERT INTO CallOperator(operID, name) VALUES (?, ?)''', (operID, name))
    # Creating Call row
    cur.execute('''INSERT INTO Call(callID, date, time, emergency, operID, name) VALUES (?, ?, ?, ?, ?, ?)''', (callID, date, time, emergency, operID, vName))
    # Creating Event row
    print(str(eventID) + " " + str(callID) + " " + str(urgency))
    cur.execute('''INSERT INTO Event(eventID, callID, urgency) VALUES (?, ?, ?)''', (eventID, callID, urgency))
    # Commit queries and exit db
    conn.commit()
    cur.close()
    conn.close()

    return callCenter()

# Pulling data from db, returning a list
def pullVictim():
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    row = cur.execute('SELECT * FROM Victim')
    row = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return list(row)


def pullCall():
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    row = cur.execute('SELECT * FROM Call')
    row = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return list(row)

def pullEvent():
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    row = cur.execute('SELECT * FROM Event')
    row = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return list(row)

# Printing Call information to make missions
@app.route('/incidentPanel')
def incidentPanel():
    # Lists will all have the same length, can combine the indexs to display all the important information
    victims = pullVictim()
    calls = pullCall()
    events = pullEvent()

    extends = '{% extends "IncidentPanel.html" %}'
    block = '{% block table %}'
    endblock = '{% endblock %}'
	# create a main list.
    mainList = []

    # get variables needed for HTML string
    for i in range(len(victims)):
        timestamp = calls[i][2] + " " + calls[i][1]
        emergency = calls[i][3]
        address = victims[i][1]
        phone = victims[i][5]
        urgency = events[i][2]
        subList = [timestamp, emergency, address, phone, urgency]
        mainList.append(subList)
    
    # generate HTML string
    htmlString = ""
    for i in range(len(mainList)):
        htmlString += "\n\t<tr class=\"data\">"
        htmlString += "\n\t\t<td>" + mainList[i][0]
        htmlString += "</td>\n\t\t<td>" + mainList[i][1]
        htmlString += "</td>\n\t\t<td>" + mainList[i][2]
        htmlString += "</td>\n\t\t<td>" + mainList[i][3]
        htmlString += "</td>\n\t\t<td>" + str(mainList[i][4])
        htmlString += "</td>\n\t</tr>"
    
	# append this htmlString to the HTML table.
    htmlString = extends + "\n" + block + htmlString + "\n" + endblock

    # overwrites existing html file
    with open("Prototype/templates/IncidentTable.html", "w") as f:
       f.write(htmlString)

    return render_template('IncidentTable.html')