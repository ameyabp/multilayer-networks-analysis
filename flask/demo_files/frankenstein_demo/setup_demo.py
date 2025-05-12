from neo4j import GraphDatabase

################################################################
# I dedicate this code to Perplexity as well!
# This is the code to set up the Frankenstein demo.
# Setup:
# 1. Make sure the URI and AUTH are correct for your Neo4j instance.
# 2. Run the command 'python setup_demo.py' to import the data.
# 3. Ensure that the Neo4j instance information is correct in Project3
# and visalize whatever this dataset's supposed to be!
# It takes a second... so uhhh you can probably add a limit to the query
# to speed it up if you want.
################################################################

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = 'bolt://localhost:7687'
AUTH = ("neo4j", "PASSWORD")

driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify connectivity when the application starts
with driver.session() as session:
    session.run("RETURN 1")

def parse_and_import():
    # Read edge data from file
    edges = []
    with open('FRANKENSTEIN_EDGES.txt', 'r') as file:
        for line in file:
            source, target = line.strip().split(',')
            edges.append({'source': source, 'target': target})

    # Bulk import using Cypher
    with driver.session() as session:
        query = """
        UNWIND $edges AS edge
        MERGE (s:Node {id: edge.source})
        MERGE (t:Node {id: edge.target})
        MERGE (s)-[:CONNECTED_TO]->(t)
        """
        session.run(query, edges=edges)

    driver.close()

if __name__ == '__main__':
    parse_and_import()