import networkx as nx


class Analyzer:
    def __init__(self, dev_flag):
        self.query = Query(dev_flag)
        self.graph = None

    def search_nodes(self, keyword):
        node = self.query.get_node_by_name(keyword)
        return node

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
        print('Calculating distance between %s and %s' % (node_source.properties['NAME'], node_target[0].properties['NAME']))
        n_j = self.get_num_rels(node_target)
        n_i_j = self.get_num_rel(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = ([1/ksp - 1])
        return d

    def analyze(self, source_node):
        paths = nx.single_source_dijkstra_path(self.graph, source_node)
        lengths = nx.single_source_dijkstra_path_length(self.graph, source_node)