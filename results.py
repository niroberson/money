from pandas import DataFrame
import pylab
import json
import networkx as nx
import os


class Results:
    def __init__(self, config, graph, concept_node):
        self.config = config
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
        for source_target in self.graph.edges():
            pass
        temp_path = os.path.join(self.config.data_dir, 'graph.json')
        json.dump(graph_data, open(temp_path, 'w'))
        # TODO: convert to json readable by sigma or cytoscape
        # Format nodes : [{id:id, name:name}]
        # Format edges : [{source:id, target:id: weight:weight}]