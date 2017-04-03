#!/bin/bash

# Export a variable to global scope so that
# Flask knows what's up.
echo Defining server application for Flask...
export FLASK_APP=server/server.py

# Start the Flask server.
echo Starting Flask...
flask run
