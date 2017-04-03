#!/usr/bin/python3
"""
File: server.py
Author: Gerard Geer
Purpose:
	This file is the basic backbone of Wakapedia. It takes requests, and sends 
    them out to the more interesting parts of the program.
"""

from flask import Flask, request
from main import main

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

@app.route('/wiki/<article>')
def serve_wikipage(article):
	"""
	Serves a wikipedia page. This is where things get real.
	
	Parameters:
	None.
	
	Returns:
	None.
	
	Preconditions:
	Not really any.

	Postconditions:
	Returns the MC Wiki page.
	"""

	return main(article)
	#return request.path
