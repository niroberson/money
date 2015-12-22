from query import Query
__author__ = 'nathir2'


class Algorithm:
    def __init__(self):
        self.query = Query()

    def search_nodes(self, keyword):
        node = self.query.get_node(keyword)
        return node[0][0]

    def get_num_rels(self, node):
        rels = self.query.get_node_rels(node)
        total = 0
        for rel in rels:
            total += int(rel[0].properties['COUNT'])
        return total

    def get_num_rel(self, node1, node2):
        rel = self.query.get_rel(node1, node2)
        return int(rel.properties['COUNT'])

    def ksp(self):
        node_of_interest = self.search_nodes("2-Acetolactate Mutase")
        N_i = self.get_num_rels(node_of_interest)
        direct_nodes = self.query.get_direct_nodes(node_of_interest)
        d = []
        for node in direct_nodes:
            print('Calculating distance for %s' % node[0].properties['NAME'])
            N_j = self.get_num_rels(node)
            N_i_j = self.get_num_rel(node_of_interest, node)
            KSP = N_i_j/(N_i+N_j-N_i_j)
            d.append([1/KSP - 1])
        return d