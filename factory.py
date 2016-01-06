from graph import Graph
from results import Results
from numba import autojit


class RecommenderFactory(object):
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
        concept_node = self.graph.get_node_by_name(concept)
        object_node = self.graph.get_node_by_name(object)

        self.graph.create_subgraph(concept_node, max_level=1)
        # Get the results
        results = Results(self.config, self.graph, concept_node)
        return results

    def search_concept_object(self, config, object):
        concept_node = self.graph.get_node_by_name(object)
        object_node = self.graph.get_node_by_name(object)

    @autojit
    def traverse_edges(self):
        edge_ids = self.graph.database.get_all_edge_ids()
        for eid in edge_ids:
            self.graph.create_edge(eid[0])

    def traverse_nodes(self):
        node_ids = self.graph.database.get_all_node_ids()
        for nid in node_ids:
            self.graph.create_node(nid[0])
