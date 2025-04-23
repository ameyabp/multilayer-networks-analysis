from flask import Flask, request, jsonify
import pandas as pd
import networkx as nx
import igraph as ig
from flask_cors import CORS


# NOTE: At least on my local machine, Flask runs at http://127.0.0.1:5000/
# TODO: Support more than just Frankenstein dataset from CSV.

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

@app.route('/random')
def rand():
    """
    Generates a random layout for a graph based on the data in 'frank_data.csv'.

    returns:
        JSON response with node coordinates in the format:
        [
            {"Node": "node1", "Long1": x1, "Lat1": y1},
            {"Node": "node2", "Long1": x2, "Lat1": y2},
            ...
        ]
    """
    return visualize_igraph("random")

@app.route('/circular')
def circular():
    """
    Generates a circular layout for a graph based on the data in 'frank_data.csv'.

    returns:
        JSON response with node coordinates in the format:
        [
            {"Node": "node1", "Long1": x1, "Lat1": y1},
            {"Node": "node2", "Long1": x2, "Lat1": y2},
            ...
        ]
    """
    return visualize_igraph("circular")

@app.route('/fruchterman_reingold')
def fr():
    """
    Generates a FR layout for a graph based on the data in 'frank_data.csv'.

    returns:
        JSON response with node coordinates in the format:
        [
            {"Node": "node1", "Long1": x1, "Lat1": y1},
            {"Node": "node2", "Long1": x2, "Lat1": y2},
            ...
        ]
    """
    return visualize_igraph("fruchterman_reingold")

@app.route('/star')
def star():
    """
    Generates a star layout for a graph based on the data in 'frank_data.csv'.

    returns:
        JSON response with node coordinates in the format:
        [
            {"Node": "node1", "Long1": x1, "Lat1": y1},
            {"Node": "node2", "Long1": x2, "Lat1": y2},
            ...
        ]
    """
    return visualize_igraph("star")

# Default route, defaults to "random as of yet"
@app.route('/')
def visualize_igraph(layout_type: str = "random"):
    """
    Generates an igraph layout for a graph based on the data in 'frank_data.csv'.

    args:
        layout_type (str): The type of layout to use. Options are "random", "circular", "fruchterman_reingold", and "star". Defaults to random.

    returns:
        JSON response with node coordinates in the format:
        [
            {"Node": "node1", "Long1": x1, "Lat1": y1},
            {"Node": "node2", "Long1": x2, "Lat1": y2},
            ...
        ]
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

    print("Laying out")
    if layout_type == "random":
        layout = g.layout_random()
    elif layout_type == "circular":
        layout = g.layout_circle()
    elif layout_type == "fruchterman_reingold":
        layout = g.layout_fruchterman_reingold()
    elif layout_type == "star":
        layout = g.layout_drl()
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

    print(edge_data)

    return jsonify((node_data, edge_data))


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()