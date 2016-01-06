import multiprocessing
from graph import Graph
from results import Results


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

    def traverse(self):
        queue = multiprocessing.Queue()
        config = self.config
        p = multiprocessing.Process(target=worker, args=(queue,))
        p.start()
        edge_ids = self.graph.database.get_all_edge_ids()
        for eid in edge_ids:
            # Instantiate a new instance graph
            queue.put([Graph(config), eid[0]])

        # Wait for the worker to finish
        queue.close()
        queue.join_thread()
        p.join()


def worker(q):
    gobj, eid = q.get()
    gobj.create_edge(eid)