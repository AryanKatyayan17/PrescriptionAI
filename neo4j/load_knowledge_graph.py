import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph=Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

graph.query("MATCH (n) DETACH DELETE n")

cypher="""
CREATE (m:Drug {name: 'Metformin', used_for: 'Type 2 Diabetes'})
CREATE (l:Drug {name: 'Lisinopril', used_for: 'Hypertension'})
CREATE (i:Drug {name: 'Ibuprofen', used_for: 'Pain relief'})
CREATE (p:Drug {name: 'Paracetamol', used_for: 'Fever and pain'})
CREATE (a:Drug {name: 'Amlodipine', used_for: 'High blood pressure'})
CREATE (az:Drug {name: 'Azithromycin', used_for: 'Bacterial infections'})

CREATE (e1:Effect {name: 'Lactic acidosis'})
CREATE (e2:Effect {name: 'Stomach upset'})
CREATE (e3:Effect {name: 'Swelling ankles'})

CREATE (m)-[:SIDE_EFFECT]->(e1)
CREATE (i)-[:SIDE_EFFECT]->(e2)
CREATE (a)-[:SIDE_EFFECT]->(e3)

CREATE (m)-[:INTERACTS_WITH]->(i)
CREATE (i)-[:INTERACTS_WITH]->(m)

CREATE (l)-[:INTERACTS_WITH]->(i)
CREATE (i)-[:INTERACTS_WITH]->(l)
"""

graph.query(cypher)
print("Drug knowledge graph loaded into Neo4j")