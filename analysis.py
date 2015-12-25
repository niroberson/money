import networkx as nx


class Analyzer:
    def __init__(self):
            pass

    def compute_distance(self, node_source, node_target, n_i):
        print('Calculating distance between %s and %s' % (node_source.properties['NAME'], node_target[0].properties['NAME']))
        n_j = self.get_num_rels(node_target)
        n_i_j = self.get_num_rel(node_source, node_target)
        ksp = n_i_j/(n_i+n_j-n_i_j)
        d = ([1/ksp - 1])
        return d

