from pandas import DataFrame
import pylab
import json
import networkx as nx
import os


class Results(object):
    def __init__(self, config, graph):
        self.config = config
        self.graph = graph
        self.table = None

    def create_table(self, concept_node, object_node=None):
        # Create table from distance results
        # Find the shortest paths in this subgraph
        nodes = self.graph.nodes()
        names = [self.graph.node[nodeX]['properties']['NAME'] for nodeX in nodes]
        data = {'Concept': names}
        self.table = DataFrame(data)

    def to_html(self):
        return self.table.to_html()

    def to_graph(self):
        pos = nx.graphviz_layout(self.graph, prog='neato')
        node_labels = {nodeX:self.graph.node[nodeX]['properties']['NAME'] for nodeX in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels)
        nx.draw_networkx_nodes(self.graph, pos, node_size=700, node_shape='o')
        nx.draw(self.graph, pos)
        if self.config.dev_flag:
            pylab.show()
        else:
            self.to_graph_json()

    def to_graph_json(self):
        graph_data = dict()
        graph_data['nodes'] = []
        # Get the nodes
        for nid in self.graph.nodes():
            name = self.graph.node[nid]['properties']['NAME']
            this_data = {'id': nid, 'name': name}
            graph_data['nodes'].append(this_data)

        # Get the edges
        graph_data['edges'] = []
        for source, target in self.graph.edges():
            e_data = self.graph.get_edge_data(source, target)
            this_data = {'source': source, 'target': target, 'type':e_data['type'], 'weight': e_data['weight']}
            graph_data['edges'].append()
        temp_path = os.path.join(self.config.data_dir, 'graph.json')
        json.dump(graph_data, open(temp_path, 'w'))
        # TODO: convert to json readable by sigma or cytoscape
        # Format nodes : [{id:id, name:name}]
        # Format edges : [{source:id, target:id: weight:weight}]