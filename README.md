# Welcome to Project3

Project3 is a network analysis and data visualization tool intended for use with both single and multilayer networks.

## Running Our Program

First, you will need to have a Neo4j instance running. Ensure you have a Neo4j database instance running, and that the ```URI``` and ```AUTH``` are set to the correctly in ```flask/app.py```. This ensures that you're correctly connected: you will be stuck on a loading screen indefinately if Neo4j does not connect.

Next, navigate to the ```flask``` directory and run the command ```python app.py```. After this, navigate to the ```frontend``` directory and run ```npm run start```. After this, you should be able to view the program by navigating to ```https://localhost:3000/```.

Alternatively on Mac or Linux, you can run the command ```./start.sh``` in the root folder to start the program. BE SURE to exit the program with ```ctrl+c``` with this command or else they might be running in the background!

## Frankenstein Demo

If you have no data to visualize, we have an example demo you can try to see how Project3 works. Based on the famous novel Frankenstein by Mary Shelly, legend has it that nobody knows what this dataset actually represents, but it looks pretty cool and you can query it.

### How to Add Frankenstein Demo Data To Your Neo4j Instance:
1. Navigate to ```flask/demo_files/frankenstein_demo```.
2. Ensure that your Neo4j database instance is running.
3. In the file ```setup_demo.py```, make sure that the ```URI```, ```password```, and ```AUTH``` are correct.
4. Run the command ```python setup_demo.py``` in your terminal.
5. Run the app and enjoy!

## Upcoming TODOS:

* Implement Korean Highway demo (i.e. implement differentiation between coordinate and non-coordinate data)
* Visualized querying
* Implement global context so we can have components!
* Multilayer & streaming data support.