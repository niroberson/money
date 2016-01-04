from graph import Graph
from results import Results


class RecommenderFactory:
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, config):
        self.graph = Graph(config)
        self.config = config

    def search_concept(self, concept):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph(concept_node, max_level=1)
        results = Results(self.config, self.graph, concept_node)
        return results

    def search_concept_predication(self, concept, predication):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph(concept_node, predication=predication, max_level=1)
        results = Results(self.config, self.graph, concept_node)
        return results

    def search_concept_predication_object(self, concept, predication, object):
        concept_node = self.graph.get_node_by_name(object)
        self.graph.create_subgraph(concept_node, max_level=1)
        # Get the results
        results = Results(self.config, self.graph, concept_node)
        return results

    def create_distance_graph(self):
        self.graph.traverse()


