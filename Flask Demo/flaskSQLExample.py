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
def showInt():
    # Reconnecting to db to print results on webpage
    db = MySQLdb.connect(host="localhost",    
                     user="root",         
                     passwd="",  
                     db="callcenter")

    cur = db.cursor()

    cur.execute("SELECT * FROM event")
    row = cur.fetchall()
    db.close()
    
    return str(row)
  
if __name__ == '__main__':
    app.run()