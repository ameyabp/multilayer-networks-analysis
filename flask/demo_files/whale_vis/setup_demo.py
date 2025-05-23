from neo4j import GraphDatabase
import csv

# Configuration
URI = 'bolt://localhost:7687'
AUTH = ("neo4j", "PASSWORD")  # Replace with your actual password

driver = GraphDatabase.driver(URI, auth=AUTH)

# Verify connection
with driver.session() as session:
    result = session.run("RETURN 1")
    print("Connected to Neo4j:", result.single())

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def parse_and_import():
    nodes = []

    # Read only Lat and Lon from the CSV
    with open('14-01-2024.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = safe_float(row.get('Lat'))
            lon = safe_float(row.get('Lon'))
            if lat is not None and lon is not None:
                nodes.append({
                    'latitude': lat,
                    'longitude': lon
                })

    # Import into Neo4j
    with driver.session() as session:
        print(f"Importing {len(nodes)} nodes into Neo4j...")
        query = """
        UNWIND $nodes AS node
        CREATE (:Location {latitude: node.latitude, longitude: node.longitude})
        """
        session.run(query, nodes=nodes)

    driver.close()
    print("Import complete.")

if __name__ == '__main__':
    parse_and_import()
