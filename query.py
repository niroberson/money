from connect import Database
__author__ = 'nathir2'


class Query:
    def __init__(self):
        self.db = Database().connect_local()

    def get_node(self, search_input):
        cypher_query = "MATCH (n { NAME:'" + search_input + "'}) RETURN n"
        return self.db.cypher.execute(cypher_query)

    def get_rels_from_node(self, node):
        cypher_query = "MATCH (n { CONCEPTID:'" + node.properties['CONCEPTID'] + "'}) RETURN n"
        return self.db.cypher.execute(cypher_query)