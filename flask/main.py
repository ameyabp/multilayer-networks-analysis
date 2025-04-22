from flask import Flask, request, jsonify
import pandas as pd
import networkx as nx
import igraph as ig
from flask_cors import CORS


# NOTE: At least on my local machine, Flask runs at http://127.0.0.1:5000/

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

@app.route('/random')
def rand():
    return visualize_frankenstein_igraph("random")

@app.route('/circular')
def circular():
    return visualize_frankenstein_igraph("circular")

@app.route('/fruchterman_reingold')
def fr():
    return visualize_frankenstein_igraph("fruchterman_reingold")

@app.route('/star')
def star():
    return visualize_frankenstein_igraph("star")

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

# So it looks like we can add routes above to have a lot of Python integrations!
@app.route('/')
def visualize_frankenstein_igraph(layout_type: str = "random"):
    """
    More details about the layout algorithms I'll be using can be found here:
    https://igraph.org/c/doc/igraph-Layout.html
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

    data = []

    for idx, (x, y) in enumerate(layout.coords):
        label = g.vs[idx]["name"] if "name" in g.vs.attributes() else idx
        data.append([label, x, y])

    df = pd.DataFrame(data, columns=["Node", "Long1", "Lat1"])
    # For now it just generates a CSV file with the layout coordinates!
    df.to_csv(f"csvs/graph_layout_{layout_type}.csv", index=False)

    print("finished adding to the stupid spreadsheet that i hate")

    # Has to return something aparently or else Flask freaks out at you! Found this out the hard way!
    return jsonify(data)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()