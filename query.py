from connect import Database
from py2neo.cypher.core import Record
__author__ = 'nathir2'


class Query:
    def __init__(self):
        self.db = Database().connect_local()
        self.dev = True

    def execute_query(self, cypher_query):
        if self.dev:
            cypher_query += " LIMIT 20"
        self.db.cypher.execute(cypher_query)

    def get_node(self, search_input):
        cypher_query = "MATCH (n:Concept { NAME:'" + search_input + "'}) RETURN n"
        return self.execute_query(cypher_query)

    def get_node_rels(self, node):
        if isinstance(node, Record):
            node = node[0]
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN r"
        return self.execute_query(cypher_query)

    def get_direct_nodes(self, node):
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN c"
        return self.execute_query(cypher_query)

    def get_rel(self, node1, node2):
        if isinstance(node1, Record):
            node1 = node1[0]
        if isinstance(node2, Record):
            node2 = node2[0]
        cypher_query = "MATCH (n:Concept { CUI:'" + node1.properties['CUI'] + "'})-[r]-(c { CUI:'" + node2.properties['CUI'] + "'})" + "RETURN r"
        return self.execute_query(cypher_query)

    def get_secondary_nodes(self, node):
        cypher_query = "MATCH (a:Concept)--(b) WHERE a.CUI = 'C0008304' OPTIONAL MATCH (b)--(c)--(d) RETURN distinct d"
        return self.execute_query(cypher_query)
