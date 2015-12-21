from connect import Database
__author__ = 'nathir2'


class Query:
    def __init__(self):
        self.db = Database().connect_local()

    def get_node(self, search_input):
        cypher_query = "MATCH (n { NAME:'" + search_input + "'}) RETURN n"
        for node in self.db.cypher.execute(cypher_query):
            print(node[0])