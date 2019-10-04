# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:25:13 2019

@author: kenny

Modified by: Joe
Date: 10/3/19

"""
"""
paste http://127.0.0.1:5000/ into browser to connect to server
"""
from flask import Flask, render_template
#Backend location
print("hello")


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Nuclear Geeks"

@app.route('/callCenter')
def callCenter():
    return render_template("callCenter.html")

@app.route('/incidentPanel')
def incidentPanel():
    return render_template('IncidentPanel.html')


if __name__ == '__main__':
    app.run()