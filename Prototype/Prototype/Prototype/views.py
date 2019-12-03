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
VID = 3000
USER = "Admin"
ID = None
NAME = None

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

# Generates new vID for Victim table
def getVID():
    global VID
    victim = pullVictim()
    ids = [x[6] for x in victim]
    while VID in ids:
        VID += 1
    return VID

def authenticate(roles):
    global USER
    if USER not in roles and USER != "Admin":
        return False

    return True

@app.route('/volunteer')
def volunteer():    
    return render_template("volunteer.html")

# run ipconfig in terminal then use the IPv4 address:5000 to access page
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    global USER
    USER = None
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    #roleCheck('Kenny')
    #addUser('Kenny', '1111', 'Volunteer')
    #userCheck('JaneDoe1')
    #passCheck('JaneDoe1', '1234')
    global USER
    global ID
    global NAME

    if request.method == 'GET':
        #id = request.form["id"]
        return render_template("loginpage.html", var=False) # var used to render invalid id/password
    if request.method == 'POST':
        id = request.form.getlist('password') # Existing User Password
        username = request.form.getlist('username') # Existing User Username
        usernameReg = request.form.getlist('usernameReg') # Registering User Username
        IDReg = request.form.getlist('IDReg') # Registering User ID
        passwordReg = request.form.getlist('passwordReg') # Registering User Password
        userTypeReg = request.form.getlist('userTypeReg') # Registering User UserType

        print(IDReg)
        #login
        if (len(id) > 0):
            username = username[0]
            id = id[0]
            if userCheck(username) == True:
                if  passCheck(username, id)== True: 
                    if roleCheck(username) == "Operator":
                        USER = "Operator"
                        ID = id
                        NAME = username
                        return redirect(url_for('callCenter'))
                    if roleCheck(username) == "Volunteer":
                        USER = "Volunteer"
                        return redirect(url_for('volunteer'))
                    if roleCheck(username) == "Manager":
                        USER = "Manager"
                        return redirect(url_for('deploymentPanel'))
                    if roleCheck(username) == "Officer":
                        USER = "Officer"
                        return redirect(url_for('incidentPanel'))
                    if roleCheck(username) == "Admin":
                        USER = "Admin"
                        return redirect(url_for(''))
                    #Possible another if for determing what page to go for each user -- Will have to check what role they are then do ifs off that
        #register
        else:

            usernameReg1 = usernameReg[0]
            IDReg1 = IDReg[0]
            userTypeReg1 = userTypeReg[0]
            print(usernameReg1)
            print(IDReg1)
            print(userTypeReg1)
            print("Test1")
            if userCheck(usernameReg1) == False:
                print("Test")
                addUser(usernameReg1, IDReg1, userTypeReg1)
                print("Test2")
                return redirect(url_for('login')) #Need to submit their data and return
            else:
                return redirect(url_for('login'))
    
    return render_template("loginpage.html")

@app.route('/callCenter', methods=['GET', 'POST'])
def callCenter():
    roles = ["Operator"]

    if not authenticate(roles):
        if USER == None:
            return redirect(url_for('login'))
        return redirect(request.referrer)

    if request.method == 'POST':
        getInfo()
    return render_template("callCenter.html")

# gets input from HTML page
def getInfo():

    global ID
    global NAME
    # variables for the Operator
    operID = ID
    name = NAME
    
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
    vID = getVID()
    # variables for Event
    urgency = request.form['Urgency']
    eventID = getEventID()
    
    # Opening db
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()

    # Adding victim info
    cur.execute('''INSERT INTO Victim (name, address, city, state, zipCode, phone, vID) VALUES (?, ?, ?, ?, ?, ?, ?)''', (vName, address, city, state, zipCode, phoneNumber, vID))
    # Adding operator info
    cur.execute('''INSERT INTO CallOperator(operID, name) VALUES (?, ?)''', (operID, name))
    # Creating Call row
    cur.execute('''INSERT INTO Call(callID, date, time, emergency, operID, vID) VALUES (?, ?, ?, ?, ?, ?)''', (callID, date, time, emergency, operID, vID))
    # Creating Event row
    #print(str(eventID) + " " + str(callID) + " " + str(urgency))
    cur.execute('''INSERT INTO Event(eventID, callID, urgency, vID) VALUES (?, ?, ?, ?)''', (eventID, callID, urgency, vID))
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
    roles = ["Operator", "Officer"]
    if not authenticate(roles):
        if USER == None:
            return redirect(url_for('login'))
        return redirect(request.referrer)

    if request.method == 'POST':
      ids = request.form.getlist('id')
      edit = request.form.getlist('edit')
      if len(edit) > 0 and edit[0] == 'edited':
        id = request.form['id']
        n = request.form['name']
        e = request.form['emergency']
        a = request.form['address']
        p = request.form['phone']
        u = request.form['urgency']
        
        # then insert edits into database
        editName(id, n)
        editEmergency(id, e)
        editAddress(id, a)
        editPhone(id, p)
        editUrgency(id, u)
        return redirect(request.referrer)

      if len(edit) > 0 and edit[0].isnumeric():
        return editTable(edit[0])

      id = request.form['delete']
      if id:
          deleteEvent(id)
          return redirect(request.referrer)

      if ids == []:
        return redirect(url_for('createMission'))

    id, timestamp, emergency, address, phone, urgency = genTable()
    length = len(id)

    return render_template('IncidentTable.html', var=False, length=length, id=id, timestamp=timestamp, emergency=emergency, address=address, phone=phone, urgency=urgency)

@app.route('/incidentPanel/edit', methods=['POST', 'GET'])
def editTable(editID):
    roles = ["Operator", "Officer"]
    if not authenticate(roles):
        if USER == None:
            return redirect(url_for('login'))
        return redirect(request.referrer)

    id, timestamp, emergency, address, phone, urgency = genTable()
    i = id.index(int(editID))
    n = pullVictim()[0][0]
    e = emergency[i]
    a = address[i]
    p = phone[i]
    u = urgency[i]
    editID = int(editID)
    return render_template('editTable.html', name=n, emergency=e, address=a, phone=p, urgency=u, id=editID)


@app.route('/incidentPanel/create')
def createMission():
   roles = ["Officer"]
   if not authenticate(roles):
        if USER == None:
            return redirect(url_for('login'))
        return redirect(request.referrer)
       
   id, timestamp, emergency, address, phone, urgency = genTable()
   length = len(id)

   return render_template('IncidentTable.html', var=True, length=length, id=id, timestamp=timestamp, emergency=emergency, address=address, phone=phone, urgency=urgency)

@app.route('/deploymentPanel', methods=['POST', 'GET'])
def deploymentPanel():
    roles = ["Officer", "Manager"]
    if not authenticate(roles):
        if USER == None:
            return redirect(url_for('login'))
        return redirect(request.referrer)

    if request.method == 'POST':
        id = request.form['delete']
        deleteEvent(id)

    missions = returnMission()
    zip = [z[0] for z in missions]
    emergency = [e[1][0][4] for e in missions]
    team = []
    status = []
    length = len(zip)
    id = [i[1][0][0] for i in missions]

    for i in range(len(zip)):
        team.append(i)
        status.append("Incomplete")

    return render_template('deploymentTable.html', length=length, zip=zip, emergency=emergency, team=team, status=status, id=id)

def getZips():
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    # Get all zipCodes
    #zips = cur.execute('SELECT DISTINCT victim.zipCode from victim inner join event on victim.name = call.name inner join call on event.callID = call.callID')
    zips = cur.execute('SELECT DISTINCT victim.zipCode from victim inner join event on victim.vID = call.vID inner join call on event.callID = call.callID')
    zips = cur.fetchall()
    #  list(zips)
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
        #names = cur.execute('SELECT name FROM victim WHERE zipCode = (?)', zips[i])
        #names = cur.fetchall()
        vIDs = cur.execute('SELECT vID FROM victim WHERE zipCode = (?)', zips[i])
        vIDs = cur.fetchall()
        vLen = len(vIDs)
        
        # Assigning zipcode with event info into a 2D list
        for j in range(vLen):
            # 3 way inner join using name
            eventInfo = cur.execute('SELECT DISTINCT event.eventID, call.vID, call.date, call.time, call.emergency, victim.address, victim.phone, event.urgency from victim inner join event on victim.vID = call.vID inner join call on event.callID = call.callID WHERE event.vID = (?)', vIDs[j])
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

def deleteEvent(eventID):
    # Deletes the event with the given eventID
    # Used for when user makes an error when typing an event
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()

    event = cur.execute('SELECT * FROM event WHERE eventID = ?', (eventID,))
    event = cur.fetchall()
    #print(event)
    #print(event[0][0])
    cur.execute('DELETE FROM victim WHERE vID = ?', (event[0][3],))
    cur.execute('DELETE FROM call WHERE callID = ?', (event[0][1],))
    cur.execute('DELETE FROM event WHERE eventID = ?', (event[0][0],))
  
    conn.commit()
    cur.close()
    conn.close()

def editEmergency(eventID, newEm):
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    

    vID = cur.execute('SELECT vID FROM event WHERE eventID = ?', (eventID,))
    vID = cur.fetchall()
 
    cur.execute('UPDATE Call SET emergency = ? WHERE vID = ?', (newEm, vID[0][0]))
    conn.commit()
    cur.close()
    conn.close()   
    
def editAddress(eventID, newAdd):
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    

    vID = cur.execute('SELECT vID FROM event WHERE eventID = ?', (eventID,))
    vID = cur.fetchall()

    cur.execute('UPDATE Victim SET address = ? WHERE vID = ?', (newAdd, vID[0][0]))
    conn.commit()
    cur.close()
    conn.close() 

def editPhone(eventID, newPhone):
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    

    vID = cur.execute('SELECT vID FROM event WHERE eventID = ?', (eventID,))
    vID = cur.fetchall()

    cur.execute('UPDATE Victim SET phone = ? WHERE vID = ?', (newPhone, vID[0][0]))
    conn.commit()
    cur.close()
    conn.close() 

def editUrgency(eventID, newUrg):
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    
    cur.execute('UPDATE Event SET urgency = ? WHERE eventID = ?', (newUrg, eventID))
    conn.commit()
    cur.close()
    conn.close() 

def editName(eventID, newName):
    conn = sqlite3.connect("callCenter.db")
    cur = conn.cursor()
    

    vID = cur.execute('SELECT vID FROM event WHERE eventID = ?', (eventID,))
    vID = cur.fetchall()

    cur.execute('UPDATE Victim SET name = ? WHERE vID = ?', (newName, vID[0][0]))
    conn.commit()
    cur.close()
    conn.close()

# Returns true is user exists, false of user's not registered
def userCheck(username):
    conn = sqlite3.connect("logins.db")
    cur = conn.cursor()

    userBool = cur.execute('SELECT username FROM users WHERE username = ?', (username,))
    userBool = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    if userBool == []:
        return False
    else:
        return True

def roleCheck(username):
    conn = sqlite3.connect("logins.db")
    cur = conn.cursor()

    userType = cur.execute('SELECT userType FROM users WHERE username = ?', (username,))
    userType = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    role = userType[0][0]
    str(role)
    return role

# Returns true is user exists, false of user's not registered
def passCheck(username, id):
    conn = sqlite3.connect("logins.db")
    cur = conn.cursor()

    passBool = cur.execute('SELECT username FROM users WHERE password = ?', (id,))
    passBool = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    if passBool == []:
        return False
    else:
        return True

def addUser(username, password, role):
    conn = sqlite3.connect("logins.db")
    cur = conn.cursor()

    cur.execute('''INSERT INTO users(username, password, userType) VALUES (?, ?, ?)''', (username, password, role))

    conn.commit()
    cur.close()
    conn.close()