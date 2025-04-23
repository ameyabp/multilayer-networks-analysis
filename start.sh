#!/bin/bash

# Start Flask
cd flask
export FLASK_APP=app.py
flask run &
FLASK_PID=$!

# Start Next.js
cd ../project3
npx next dev &
NEXT_PID=$!

# Trap EXIT (script ends) and INT/TERM (Ctrl+C/kill) to kill background jobs
trap "kill $FLASK_PID $NEXT_PID" EXIT INT TERM

# Wait for background jobs to finish (keeps script running)
wait