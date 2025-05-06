from flask import Flask, request, jsonify
import pandas as pd
import networkx as nx
import igraph as ig
from flask_cors import CORS
from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = 'bolt://localhost:7687'
AUTH = ("neo4j", "PASSWORD")

driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify connectivity when the application starts
with driver.session() as session:
    session.run("RETURN 1")

# NOTE: At least on my local machine, Flask runs at http://127.0.0.1:5000/
# TODO: Support more than just Frankenstein dataset from CSV.

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Documentation I used: https://neo4j.com/docs/python-manual/current/
@app.route('/query/<query_string>/')
def query_neo4j(query_string: str):
    """
    Returns a JSON response with the data from the Neo4j database.

    returns:
        JSON response with the data from the Neo4j database.
    """
    with driver.session(database="neo4j") as session:
        result = session.run(query_string)
        data = [record.data() for record in result]

    return jsonify(data)

# Route for layouts
@app.route('/getlayout/<layout_type>/')
def visualize_igraph(layout_type: str = "random"):
    """
    Generates an igraph layout for a graph based on the data in 'frank_data.csv'.

    args:
        layout_type (str): The type of layout to use. Supports most layouts listed in igraph documentation.
            Please note that the input is simply the last word in the function name (i.e. to use "igraph.layout_random", use "random" as the input).
            Defaults to "random", and has following options:
            - random
            - circle
            - fruchterman_reingold
            - star
            - grid
            - kamada_kaway
            - graphopt
            - drl
            - davidson_harel
            - sugiyama

    returns:
        JSON response with a tuple containing node data & edge data.
    """    

    try:
        df = pd.read_csv('frank_data.csv')
    except FileNotFoundError:
        print("Error: Uhhh... I do't see a 'frank_data.csv' file in this folder...")
    
    G = nx.Graph()
    
    # Add nodes and edges from the subset of data
    for _, row in df.iterrows():
        graph_id = row['graph_id']
        nodes = row['nodes'].split(';')
        edges = row['edges'].split(';') if isinstance(row['edges'], str) else []
        
        # Add nodes for this graph
        G.add_nodes_from(nodes)
        
        # Add edges for this graph
        for edge in edges:
            src, tgt = edge.split('-')
            G.add_edge(src, tgt)

    # I created a NetworkX graph above, but the cool thing is we can convert it to an igraph graph so
    # it doesn't take 20 hours to process!
    g = ig.Graph.from_networkx(G)

    # So many if statements!!
    print("Laying out")
    if layout_type == "random":
        layout = g.layout_random()
    elif layout_type == "circle":
        layout = g.layout_circle()
    elif layout_type == "fruchterman_reingold":
        layout = g.layout_fruchterman_reingold()
    elif layout_type == "star":
        layout = g.layout_star()
    elif layout_type == "grid":
        layout = g.layout_grid()
    elif layout_type == "drl":
        layout = g.layout_drl()
    elif layout_type == "kamada_kawai":
        layout = g.layout_kamada_kawai()
    elif layout_type == "graphopt":
        layout = g.layout_graphopt()
    elif layout_type == "davidson_harel":
        layout = g.layout_davidson_harel()
    elif layout_type == "sugiyama":
        layout = g.layout_sugiyama()
    else:
        print(f"Unknown layout type: {layout_type}")
        return

    print("Finished laying out")

    node_data = []
    edge_data = []

    # Get node positions
    for idx, (x, y) in enumerate(layout.coords):
        label = g.vs[idx]["name"] if "name" in g.vs.attributes() else idx
        node_data.append([label, x, y])

    # Get edge list as pairs of indices
    edges = g.get_edgelist()

    # If you want edge coordinates (for plotting):
    edge_data = [ [layout[source], layout[target]] for source, target in edges ]
    return jsonify((node_data, edge_data))

from flask import Flask, request, jsonify
import atexit

# Close the Neo4j driver when the application shuts down
def close_driver():
    if driver:
        driver.close()

atexit.register(close_driver)

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()