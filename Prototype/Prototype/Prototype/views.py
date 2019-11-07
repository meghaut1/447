"""
Routes and views for the flask application.
"""
# https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
# Use the above link if you would like to change the formatting of date or time
from datetime import datetime
from flask import render_template, g, request, redirect, url_for
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


# run ipconfig in terminal then use the IPv4 address:5000 to access page
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form["id"]
        return render_template("loginpage.html", var=False) # var used to render invalid id/password

    return render_template("loginpage.html")

@app.route('/callCenter', methods=['GET', 'POST'])
def callCenter():
    #returnMission() # used for testing
    if request.method == 'POST':
        getInfo()
    return render_template("callCenter.html")

# gets input from HTML page
def getInfo():

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

def genTable():
     # Lists will all have the same length, can combine the indexs to display all the important information
    victims = pullVictim()
    calls = pullCall()
    events = pullEvent()

    id = []
    timestamp = []
    emergency = []
    address = []
    phone = []
    urgency = []

    for i in range(len(victims)):
        id.append(events[i][0])
        timestamp.append(calls[i][2] + " " + calls[i][1])
        emergency.append(calls[i][3])
        address.append(victims[i][1])
        phone.append(victims[i][5])
        urgency.append(events[i][2])

    return id, timestamp, emergency, address, phone, urgency

# Printing Call information to make missions
@app.route('/incidentPanel', methods=['POST', 'GET'])
def incidentPanel():
    
    if request.method == 'POST':
      ids = request.form.getlist('id')
      if ids == []:
        return redirect(url_for('createMission'))

    id, timestamp, emergency, address, phone, urgency = genTable()
    length = len(id)

    return render_template('IncidentTable.html', var=False, length=length, id=id, timestamp=timestamp, emergency=emergency, address=address, phone=phone, urgency=urgency)

@app.route('/incidentPanel/create')
def createMission():
   id, timestamp, emergency, address, phone, urgency = genTable()
   length = len(id)

   return render_template('IncidentTable.html', var=True, length=length, id=id, timestamp=timestamp, emergency=emergency, address=address, phone=phone, urgency=urgency)


def getZips():
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    # Get all zipCodes
    zips = cur.execute('SELECT DISTINCT victim.zipCode from victim inner join event on victim.name = call.name inner join call on event.callID = call.callID')
    zips = cur.fetchall()
    #list(zips)
    #for i in range(len(zips)):
    #    zips[i] = zips[i][0]
    conn.commit()
    cur.close()
    conn.close()
    return zips

def returnMission():
    # query the event table by zipcode
    # return results in a list of strings
    # print strings in mission table
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    missions = []
    # Get all zipCodes
    zips = getZips()
    zipLen = len(zips)

    # Get all names    
    missionIndex = 0
    for i in range(zipLen):
        # Returning names for the i'th zipcode
        names = cur.execute('SELECT name FROM victim WHERE zipCode = (?)', zips[i])
        names = cur.fetchall()
        nameLen = len(names)
        
        # Assigning zipcode with event info into a 2D list
        for j in range(nameLen):
            # 3 way inner join using name
            eventInfo = cur.execute('SELECT DISTINCT event.eventID, call.name, call.date, call.time, call.emergency, victim.address, victim.phone, event.urgency from victim inner join event on victim.name = call.name inner join call on event.callID = call.callID WHERE event.vname = (?)', names[j])
            eventInfo = cur.fetchall()
            # Adding new index for 2D list
            missions.append([])
            # Converting zipcode from tuple to int
            zip = zips[i][0]
            # Appending zipcode and event 
            missions[missionIndex].append(zip)
            missions[missionIndex].append(eventInfo)
            missionIndex += 1
    
    #print(missions)
    conn.commit()
    cur.close()
    conn.close()
    # returns 2D list; 1st index of an element is the zipcode, 2nd is the event 
    return missions
