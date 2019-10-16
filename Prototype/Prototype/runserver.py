"""
This script runs the Prototype application using a development server.
"""

from os import environ
from Prototype import app

if __name__ == '__main__':
    host = '0.0.0.0' # uses host machine's IP address
    app.run(host, debug = True)
