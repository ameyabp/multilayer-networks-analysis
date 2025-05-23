from flask import Flask, request, jsonify
import networkx as nx
import igraph as ig
from flask_cors import CORS
from neo4j import GraphDatabase
import atexit

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = 'bolt://localhost:7687'
AUTH = ("neo4j", "PASSWORD")

driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify connectivity when the application starts
with driver.session() as session:
    session.run("RETURN 1")

# NOTE: At least on my local machine, Flask runs at http://127.0.0.1:5000/

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Route for layouts
# TODO: Fix to better distiguish between query types
@app.route('/getlayout/<layout_type>/')
@app.route('/getlayout/<layout_type>/<query_string>/')
@app.route('/getlayout/<layout_type>/<query_string>/<limit>/')
def visualize_igraph(layout_type: str = "random", query_string: str = """MATCH (n)-[r]->(m) RETURN n.id AS source, m.id AS target""", limit: int = 1000000):
    """
    Generates an igraph layout for a graph based on the data in 'frank_data.csv'.

    args:
        layout_type (str): The type of layout to use. Supports most layouts listed in igraph documentation.
            Please note that the input is simply the last word in the function name (i.e. to use "igraph.layout_random", use "random" as the input).
            Defaults to "random", and has following options:
            - default (if coordinates exist, will return "grid" layout if otherwise)
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
        # I would like to dedicate this code to Perplexity
        CYPHER_QUERY = query_string
        
        G = nx.Graph()
        

        ######################################################################
        # Potential Soluitions For Querying:
        # - Parsing the query string to find return type? (i.e. edges or node)
        # - Differentiating between querys upon return from Neo4j database?
        #      - Could make helper functions for each type of query?
        ######################################################################

        if query_string == "GET_EVERYTHING":
        # No matter what, save this as it returns everything in the database!
            with driver.session() as session:
                        CYPHER_QUERY = "MATCH(n) RETURN (n.id) LIMIT " + str(limit)
                        result = session.run(CYPHER_QUERY)
                        for record in result:
                            G.add_node(record)
                        # Fetch data from Neo4j
                        CYPHER_QUERY = "MATCH (n)-[r]->(m) RETURN n.id AS source, m.id AS target LIMIT " + str(limit)
                        result = session.run(CYPHER_QUERY)
                        # Process results and build graph
                        for record in result:
                            # TODO: CHANGE THIS
                            src = record["source"]
                            tgt = record["target"]
                            G.add_node(src)
                            G.add_node(tgt)
                            G.add_edge(src, tgt)
        else:
            isEdgeQuery = False
            if "AS source" in query_string and "AS target" in query_string:
                isEdgeQuery = True
            if isEdgeQuery:
                result = session.run(query_string)
                # Process results and build graph
                for record in result:
                    # CHANGE THIS
                    src = record["source"]
                    tgt = record["target"]
                    G.add_node(src)
                    G.add_node(tgt)
                    G.add_edge(src, tgt)
            else:
                result = session.run(query_string)
                for record in result:
                    G.add_node(record)
                        
    except Exception as e:
        print(f"Neo4j connection error: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.close()

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

# TODO: FIX!!! VERY ROUGH!!
@app.route('/getcoordinates/<query_string>/<int:limit>/', methods=['GET'])
@app.route('/getcoordinates/<query_string>/', methods=['GET'])
def get_coordinates(query_string, limit=1000):

    # NOTE: Don't really use the limit for the whalevis data quite yet, while we aren't using data temporally it will
    # repeat a lot of the same coordinates! I had this issue for way too long...
    try:
        coords = []
        # Optional: sanitize or decode query_string here if needed

        with driver.session() as session:
            result = session.run(query_string)
            id = 0
            for record in result:
                lat = None
                lon = None
                
                # Extract latitude and longitude
                for key in record.keys():
                    if key.lower() in ['lat', 'latitude']:
                        lat = float(record[key])
                    if key.lower() in ['lon', 'longitude']:
                        lon = float(record[key])
                    if lat is not None and lon is not None:
                        id += 1
                        coords.append([id, lat, lon])

        return jsonify(coords, [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def close_driver():
    if driver:
        driver.close()

atexit.register(close_driver)

if __name__ == '__main__':
    app.run()

# NOTE: Below is the original code for the whale vis demo. I simplified it a bit for the screenshot
# used on the research poster!
# def parse_and_import():
#     # Read edge data from file
#     nodes = []
    
#     with open('NA 14-01-2024.csv', 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             nodes.append({
#                 'CBt': row["ï»¿CBt"],
#                 'Day': row['Day'],
#                 'Mon': row['Mon'],
#                 'Year': row['Year'],
#                 'Sp': row['Sp'],
#                 'Len': row['Len'],
#                 'Lu': row['L-u'],
#                 'Sx': row['Sx'],
#                 'NoF': row['NoF'],
#                 'F1L': row['F1-L'],
#                 'F1S': row['F1-S'],
#                 'F2L': row['F2-L'],
#                 'F2S': row['F2-S'],
#                 'Fu': row['F-u'],
#                 'Lat': row['Lat'],
#                 'Lon': row['Lon'],
#                 'Exp': row['Exp'],
#                 'SumEx': row['Sum-Ex'],
#                 'Nt': row['Nt'],
#                 'SCo': row['SCo'],
#             })
            
#     # Bulk import using Cypher
#     with driver.session() as session:
#         query = """
#         UNWIND $nodes AS nodes
#         CREATE (:Node {CBt: toFloat(nodes.CBt), Day: toFloat(nodes.Day), Mon: toFloat(nodes.Mon), Year: toFloat(nodes.Year), Sp: toFloat(nodes.Sp), Len: toFloat(nodes.Len), Lu: toFloat(nodes.Lu), Sx: toFloat(nodes.Sx), NoF: toFloat(nodes.NoF), F1L: toFloat(nodes.F1L), F1S: toFloat(nodes.F1S), F2L:toFloat( nodes.F2L), F2S: toFloat(nodes.F2S), Fu: toFloat(nodes.Fu), latitude: toFloat(nodes.Lat), longitude: toFloat(nodes.Lon), Exp: toFloat(nodes.Exp), SumEx: toFloat(nodes.SumEx), Nt: toFloat(nodes.Nt), Sco: toFloat(nodes.Sco)})
#         """
#         session.run(query, nodes=nodes)

#     driver.close()