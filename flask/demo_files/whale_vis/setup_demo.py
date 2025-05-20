from neo4j import GraphDatabase
import csv

################################################################
# This is the code to set up the whale_vis demo.
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
    result = session.run("RETURN 1")
    print(result.single())

def parse_and_import():
    # Read edge data from file
    nodes = []
    
    with open('NA 14-01-2024.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nodes.append({
                'CBt': row["ï»¿CBt"],
                'Day': row['Day'],
                'Mon': row['Mon'],
                'Year': row['Year'],
                'Sp': row['Sp'],
                'Len': row['Len'],
                'Lu': row['L-u'],
                'Sx': row['Sx'],
                'NoF': row['NoF'],
                'F1L': row['F1-L'],
                'F1S': row['F1-S'],
                'F2L': row['F2-L'],
                'F2S': row['F2-S'],
                'Fu': row['F-u'],
                'Lat': row['Lat'],
                'Lon': row['Lon'],
                'Exp': row['Exp'],
                'SumEx': row['Sum-Ex'],
                'Nt': row['Nt'],
                'SCo': row['SCo'],
            })
            
    # Bulk import using Cypher
    with driver.session() as session:
        query = """
        UNWIND $nodes AS nodes
        CREATE (:Node {CBt: toFloat(nodes.CBt), Day: toFloat(nodes.Day), Mon: toFloat(nodes.Mon), Year: toFloat(nodes.Year), Sp: toFloat(nodes.Sp), Len: toFloat(nodes.Len), Lu: toFloat(nodes.Lu), Sx: toFloat(nodes.Sx), NoF: toFloat(nodes.NoF), F1L: toFloat(nodes.F1L), F1S: toFloat(nodes.F1S), F2L:toFloat( nodes.F2L), F2S: toFloat(nodes.F2S), Fu: toFloat(nodes.Fu), Latitude: toFloat(nodes.Lat), Longitude: toFloat(nodes.Lon), Exp: toFloat(nodes.Exp), SumEx: toFloat(nodes.SumEx), Nt: toFloat(nodes.Nt), Sco: toFloat(nodes.Sco)})
        """
        session.run(query, nodes=nodes)

    driver.close()

if __name__ == '__main__':
    parse_and_import()