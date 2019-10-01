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

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="callcenter")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM event")

# print all the first cell of all the rows
all_rows = cur.fetchall()
print(all_rows)

db.close()
print("hello")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello Nuclear Geeks"

if __name__ == '__main__':
    app.run()