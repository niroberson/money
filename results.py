from pandas import DataFrame
import pylab
import json
import networkx as nx
from networkx.readwrite import json_graph

class Results:
    def __init__(self, path_nodes, names, path_lengths, path_names):
        data = {'Concept': names,
                'Distance': path_lengths, 'Path': path_names}
        df = DataFrame(data, index=path_nodes)
        self.df = df.sort('Distance')

    def to_html(self):
        # Create table from distance results
        return self.df.to_html()

    def to_graph(self, graph):
        pos = nx.random_layout(graph)
        node_labels = {nodeX:graph.node[nodeX]['properties']['NAME'] for nodeX in graph.nodes()}
        nx.draw_networkx_labels(graph, pos, labels=node_labels)
        nx.draw_networkx_nodes(graph, pos, node_size=700, node_shape='d')
        pylab.show()

    def to_graph_json(self, graph):
        d = json_graph.node_link_data(graph) # node-link format to serialize
        # write json
        json.dump(d, open('graph.json', 'w'))
