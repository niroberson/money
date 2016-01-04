from graph import Graph
from results import Results


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, config):
        self.graph = Graph(config)
        self.config = config

    def search_concept(self, concept):
        # Get the node for this concept
        concept_node = self.graph.get_node_by_name(concept)

        # Create the sub-graph around this concept node
        self.graph.create_subgraph(concept_node)

        # Get the results
        results = Results(self.config, self.graph, concept_node)
        return results

    def create_distance_graph(self):
        self.graph.traverse()


