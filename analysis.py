from query import Query


class Analyzer:
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
        return int(rel[0][0].properties['COUNT'])

    def compute_distance(self, node_source, node_target, n_i):
        print('Calculating distance for %s' % node_target[0].properties['NAME'])
        n_j = self.get_num_rels(node_target)
        n_i_j = self.get_num_rel(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = ([1/ksp - 1])
        return d

    def compute_distances_single_source_node(self, keyword):
        node_of_interest = self.search_nodes(keyword)
        n_i = self.get_num_rels(node_of_interest)
        direct_nodes = self.query.get_direct_nodes(node_of_interest)
        d = []# TODO: Change to graph object with source - target - distance
        for node in direct_nodes:
            d.append(self.compute_distance(node_of_interest, node, n_i))
        return d