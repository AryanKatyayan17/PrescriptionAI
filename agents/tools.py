import os
import re
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_neo4j import Neo4jGraph

load_dotenv()

embedding_model=OpenAIEmbeddings()
faiss_db=FAISS.load_local("vector_store/patient_records_index",embedding_model,allow_dangerous_deserialization=True)
retriever=faiss_db.as_retriever(search_type="similarity",k=3)

graph=Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

def retrieve_medical_history(query:str) -> str:
    results=retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in results])

medical_history_tool=Tool(
    name="MedicalHistoryRetriever",
    func=retrieve_medical_history,
    description="Use this to retrieve relevant medical history from patient records"
)

def lookup_drug_info(drug_name:str) -> str:
    cypher=f"""
    MATCH (d:Drug)
    WHERE toLower(d.name)=toLower('{drug_name}')
    RETURN d.name AS name, d.used_for AS used_for
    """
    result=graph.query(cypher)
    if result:
        return f"{result[0]['name']} is used for {result[0]['used_for']}."
    return "Drug not found."

drug_lookup_tool=Tool(
    name="DrugLookup",
    func=lookup_drug_info,
    description="Use this to lookup what a drug is used for."
)

def check_interaction(input_str:str) -> str:
    candidates = re.findall(r"\b[A-Z][a-z]+(?:[a-z]+)?\b", input_str)

    if len(candidates) < 2:
        return "Please mention at least two drug names."

    drug1,drug2 = candidates[:2]

    cypher=f"""
    MATCH (d1:Drug)-[:INTERACTS_WITH]->(d2:Drug)
    WHERE toLower(d1.name)=toLower($drug1) AND toLower(d2.name)=toLower($drug2)
    RETURN d1.name AS drug1, d2.name AS drug2
    """
    result=graph.query(cypher,params={"drug1":drug1,"drug2":drug2})
    if result:
        return f"{drug1} interacts with {drug2}."
    return f"No known interaction between {drug1} and {drug2}."

interaction_checker_tool=Tool(
    name="InteractionChecker",
    func=check_interaction,
    description="Check if two drugs have any known interaction, use formnat: 'drug1 and drug2"
)

def lookup_side_effects(drug_name:str) -> str:
    cypher=f"""
    MATCH (d:Drug)-[:SIDE_EFFECT]->(e:Effect)
    WHERE toLower(d.name)=toLower('{drug_name}')
    RETURN e.name AS effect
    """
    result=graph.query(cypher)
    if result:
        effects=[row['effect'] for row in result]
        return f"Common side effects of {drug_name} include: {', '.join(effects)}."
    return f"No recorded side effects found for {drug_name}."

side_effect_tool=Tool(
    name="SideEffectLookup",
    func=lookup_side_effects,
    description="Use this to look up side effects of a drug. Input should be the drug name (e.g., 'Ibuprofen')."
)


TOOLS=[
    medical_history_tool,
    drug_lookup_tool,
    interaction_checker_tool,
    side_effect_tool
]