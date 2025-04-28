import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,AgentType
from agents.tools import TOOLS,retriever

load_dotenv()

llm=ChatOpenAI(
    temperature=0.2,
    model="gpt-4o"
)

agent=initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

def run_agent(query:str):
    print("Running agent...")

    faiss_docs=retriever.get_relevant_documents(query)
    context="\n\n".join([doc.page_content for doc in faiss_docs])

    final_response=agent.run(query)
    return final_response,context