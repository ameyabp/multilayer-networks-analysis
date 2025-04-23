#!/bin/bash

# Activates Flask virtual environment and start Flask server
cd flask
export FLASK_APP=app.py
flask run &

# Activates our NextJS App
cd ../project3
npx next dev &