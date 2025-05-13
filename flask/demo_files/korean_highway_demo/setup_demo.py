from neo4j import GraphDatabase
import csv

################################################################
# I dedicate this code to Perplexity as well!
# This is the code to set up the Frankenstein demo.
# Setup:
# 1. Make sure the URI and AUTH are correct for your Neo4j instance.
# 2. Run the command 'python setup_demo.py' to import the data.
# 3. Ensure that the Neo4j instance information is correct in Project3
# and see the beauty of the Korean highway system!
################################################################

URI = 'bolt://localhost:7687'
AUTH = ("neo4j", "PASSWORD")

driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify connectivity when the application starts
with driver.session() as session:
    session.run("RETURN 1")

# I love you Perplexity!
def parse_and_import():
    edges = []
    with open('FRANKENSTEIN_EDGES.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            edges.append({
                'OID': row['OID'],
                'From_Name': row['From_Name'],
                'To_Name': row['To_Name'],
                'From_No': row['From_No'],
                'To_No': row['To_No'],
                'Long1': row['Long1'],
                'Lat1': row['Lat1'],
                'Long2': row['Long2'],
                'Lat2': row['Lat2'],
                'Revised_Distance': row['Revised Distance']
            })

    with driver.session() as session:
        query = """
        UNWIND $edges AS edge
        MERGE (f:Node {id: edge.From_No, name: edge.From_Name, 
                longitude: toFloat(edge.Long1), latitude: toFloat(edge.Lat1)})
        MERGE (t:Node {id: edge.To_No, name: edge.To_Name, 
                longitude: toFloat(edge.Long2), latitude: toFloat(edge.Lat2)})
        MERGE (f)-[:CONNECTED_TO {distance: toFloat(edge.Revised_Distance)}]->(t)
        """
        session.run(query, edges=edges)

    driver.close()

if __name__ == '__main__':
    parse_and_import()