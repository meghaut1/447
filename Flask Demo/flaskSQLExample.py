# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:25:13 2019

@author: kenny
"""
"""
paste http://127.0.0.1:5000/ into browser to connect to server
"""
from flask import Flask
import MySQLdb
app = Flask(__name__)

# Backend functions
# Can edit the db on the backend
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",           # your password
                     db="callcenter")     # name of the data base

cur = db.cursor()

cur.execute("SELECT * FROM event")

# print all the first cell of all the rows
all_rows = list(cur.fetchall())
print(all_rows)

db.close()

# Frontend functions
@app.route('/')
def showDB():
    # Reconnecting to db to print results on webpage
    db = MySQLdb.connect(host="localhost",    
                     user="root",         
                     passwd="",  
                     db="callcenter")

    cur = db.cursor()

    cur.execute("SELECT * FROM event")
    row = cur.fetchall()
    db.close()
    ret = "Event 0: ID, Address, Service, Urgency, Date, Time, Zipcode<br/>"
    count = 0
    for i in row:
        count += 1
        ret +="Event " + str(count) + ": " + str(i[0]) + ", " \
        + str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " \
        + str(i[4]) + ", " + str(i[5]) + ", " + str(i[6]) + "<br/>"
     
    return str(ret)
    #return "event 1: " + str(row[0]) + "<br/>event 2: " + str(row[1])

  
if __name__ == '__main__':
    app.run()