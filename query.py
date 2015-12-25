from connect import Database
from py2neo.cypher.core import Record


class Query:
    def __init__(self, dev_flag=False):
        self.db = Database().connect_local()
        self.dev = dev_flag

    def execute_query(self, cypher_query):
        if self.dev:
            cypher_query += " LIMIT 5"
        return self.db.cypher.execute(cypher_query)

    def get_node_by_name(self, search_input):
        cypher_query = "MATCH (n:Concept { NAME:'" + search_input + "'}) RETURN n"
        node = self.db.cypher.execute(cypher_query)
        return node.one

    def get_node_by_id(self, node):
        cypher_query = ""
        return self.db.cypher.execute(cypher_query)

    def get_direct_edges(self, node):
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN r"
        return self.execute_query(cypher_query)

    def get_direct_nodes(self, node):
        cypher_query = "MATCH (n:Concept { CUI:'" + node.properties['CUI'] + "'})-[r]-c RETURN c"
        return self.execute_query(cypher_query)

    def get_edges_between_nodes(self, node1, node2):
        # Not necessarily one edge between nodes can't take [0] need to specify rel label
        cypher_query = "MATCH (n:Concept { CUI:'" + node1.properties['CUI'] + "'})-[r]-(c { CUI:'" + node2.properties['CUI'] + "'})" + "RETURN r"
        return self.execute_query(cypher_query)