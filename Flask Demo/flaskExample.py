# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:25:13 2019

@author: kenny
"""
"""
paste http://127.0.0.1:5000/ into browser to connect to server
"""

from flask import Flask


print("hello")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello Nuclear Geeks"

if __name__ == '__main__':
    app.run()