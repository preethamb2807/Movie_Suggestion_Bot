import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from graphdb import url,username, password

def get_api_key(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

os.environ["GOOGLE_API_KEY"] = get_api_key("key.txt")
os.environ["NEO4J_URI"] = url
os.environ["NEO4J_USERNAME"] = username
os.environ["NEO4J_PASSWORD"] = password

def main(query):
    graph = Neo4jGraph()
    print(graph.schema)
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro')
    chain = GraphCypherQAChain.from_llm(
        graph = graph,
        llm = llm,
        verbose = True,
        allow_dangerous_requests=True
    )
    response = chain.invoke({"query": query})
    return response['result']

def query(user_query):
    result = main(user_query)
    return result