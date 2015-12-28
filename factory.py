from graph import Graph
from results import Results


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, dev_flag):
        self.graph = Graph(dev_flag)

    def search_concept(self, concept):
        # Get the node for this concept
        concept_node = self.graph.get_node_by_name(concept)

        # Create the sub-graph around this concept node
        self.graph.create_subgraph(concept_node)

        # Get the results
        results = Results(self.graph, concept_node)

        error = None
        return results, error


