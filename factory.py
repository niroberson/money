from graph import Graph
from results import Results
from pandas import DataFrame


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.graph = Graph(dev_flag)

    def search_concept(self, concept):
        # Get the node for this concept
        concept_node = self.graph.get_node_by_name(concept)

        # Create the subgraph around this concept node
        self.graph.create_subgraph(concept_node)

        # Find the shortest paths in this subgraph
        paths, path_lengths = self.graph.get_shortest_paths(concept_node)

        # Create results
        path_nodes = path_lengths.keys()
        names = [self.graph.node[nodeX]['properties']['NAME'] for nodeX in path_nodes]
        path_names = [paths[nodeX] for nodeX in path_nodes]
        paths_lengths_l = [path_lengths[nodeX] for nodeX in path_nodes]
        results = Results(path_nodes, names, paths_lengths_l, path_names)

        error = None
        return results, error


