from pandas import DataFrame
import pylab
import json
import networkx as nx
from networkx.readwrite import json_graph
import os

class Results:
    def __init__(self, graph, concept_node):
        self.graph = graph
        self.table = None
        self.create_table(concept_node)

    def create_table(self, concept_node):
        # Create table from distance results
        # Find the shortest paths in this subgraph
        paths, path_lengths = self.graph.get_shortest_paths(concept_node)

        # Create results in data frame
        path_nodes = path_lengths.keys()
        names = [self.graph.node[nodeX]['properties']['NAME'] for nodeX in path_nodes]
        path_names = [paths[nodeX] for nodeX in path_nodes]
        paths_lengths_l = [path_lengths[nodeX] for nodeX in path_nodes]
        data = {'Concept': names,
                'Distance': paths_lengths_l,
                'Path': path_names}
        table = DataFrame(data, index=path_nodes)
        self.table = table.sort('Distance')

    def to_html(self):
        return self.table.to_html()

    def to_graph(self):
        pos = nx.random_layout(self.graph)
        node_labels = {nodeX:self.graph.node[nodeX]['properties']['NAME'] for nodeX in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels)
        nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_shape='o')
        pylab.show()

    def to_graph_json(self):
        attr = dict(id='ids', source='source', target='target', key='key')
        d = json_graph.node_link_data(self.graph, attr) # node-link format to serialize
        # write json
        gpath = os.path.join(os.path.abspath('graph.py'), 'static', 'graph.json')
        json.dump(d, open(gpath, 'w'))

    def to_graph_gexf(self):
        nx.write_gexf(self.graph, "graph.gexf")
