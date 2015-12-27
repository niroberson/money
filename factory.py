from graph import Graph
from results import Results

class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.graph = Graph(dev_flag)

    def search_concept(self, concept):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph_from_source(concept_node)

        # Get a dictionary of the shortest paths based on this node
        paths = self.graph.get_shortest_paths(concept_node)
        # Return a table sorted by shortest path lengths


