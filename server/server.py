"""
File: server.py
Author: Gerard Geer
Purpose:
	This file is the basic backbone of Wakapedia. It takes requests, and sends 
    them out to the more interesting parts of the program.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def serve_homepage():
	"""
	Serves the wikipedia homepage. We don't really need to do anything here.
	
	Parameters:
	None.
	
	Returns:
	None.

	Preconditions:
	Flask is here.
	
	Postconditions:
	Will return the wikipedia homepage.
	"""
	return 'homepage'
