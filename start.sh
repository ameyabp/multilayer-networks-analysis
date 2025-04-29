#!/bin/bash

# Start Flask
cd flask
export FLASK_APP=app.py
flask run &
FLASK_PID=$!

docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j &
NEO4J_PID=$!

# Start React
cd ../frontend
npm run start &
REACT_PID=$!



# Trap EXIT (script ends) and INT/TERM (Ctrl+C/kill) to kill background jobs
trap "kill $FLASK_PID $REACT_PID $NEO4J_PID" EXIT INT TERM

# Wait for background jobs to finish (keeps script running)
wait