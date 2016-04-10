from graph import Graph
from results import Results
from analyzer import Analyzer


class RecommenderFactory(object):
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, config):
        self.config = config
        self.graph = Graph(config)
        self.analyzer = Analyzer(config)

    def search_concept(self, concept):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph(concept_node, max_level=1)
        results = Results(self.config, self.graph)
        results.create_table(concept_node)
        return results

    def search_concept_predication(self, concept, predication):
        concept_node = self.graph.get_node_by_name(concept)
        self.graph.create_subgraph(concept_node, predication=predication, max_level=1)
        results = Results(self.config, self.graph)
        results.create_table(concept_node)
        return results

    def search_concept_predicate_object(self, concept, predication, object):
        concept_node = self.graph.get_node_by_name(concept)
        object_node = self.graph.get_node_by_name(object)
        self.graph.get_edge_by_predication(concept_node, predication, object_node)
        self.graph.load_nodes_from_source(object_node, max_level=1)
        self.graph.load_source_edges(object_node)
        self.graph.load_source_edges(concept_node)
        # Get the results
        results = Results(self.config, self.graph)
        results.create_table(concept_node)
        return results

    def search_concept_object(self, concept, object):
        concept_node = self.graph.get_node_by_name(concept)
        object_node = self.graph.get_node_by_name(object)
        # Get all direct and indirect paths connecting the two nodes
        self.graph.connect_two_nodes(concept_node, object_node)
        results = Results(self.config, self.graph)
        results.create_table(concept_node, object_node)
        return results
