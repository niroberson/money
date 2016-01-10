from graph import Graph
from results import Results
import os, csv


class RecommenderFactory(object):
    # factory class to use analyzer, graph, query, and results class
    def __init__(self, config):
        self.graph = Graph(config)
        self.config = config

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

    def search_concept_predication_object(self, concept, predication, object):
        concept_node = self.graph.get_node_by_name(concept)
        object_node = self.graph.get_node_by_name(object)
        self.graph.get_edge_by_predication(concept_node, predication, object_node)
        self.graph.load_nodes_from_source(object_node, max_level=1)
        self.graph.load_source_edges(object_node)
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

    def traverse_edges_to_csv(self):
        edge_ids = self.graph.database.get_all_edge_ids()
        count = 0
        with open(os.path.join(self.config.data_dir, 'rels.csv'), 'w', newline='\n') as file:
            fieldnames = ['start:id', 'end:id', 'RELTYPE', 'COUNT', 'DISTANCE']
            writer = csv.DictWriter(file, delimiter='\t', quoting=csv.QUOTE_NONE, fieldnames=fieldnames)
            writer.writeheader()
            for eid in edge_ids:
                count += 1
                this_edge = self.graph.create_edge(eid[0])
                writer.writerow({'start:id':this_edge.source_node.id, 'end:id':this_edge.target_node.id,
                                'RELTYPE':this_edge.type,'COUNT':this_edge.properties['COUNT'], 'DISTANCE':this_edge.distance})

                # Counter
                if count % 100 == 0:
                    print('On edge %i of %i' % (count, len(edge_ids)))

    def traverse_edges_to_neo(self):
        edge_ids = self.graph.database.get_all_edge_ids()
        count = 0
        for eid in edge_ids:
            count += 1
            this_edge = self.graph.create_edge(eid[0])
            # Counter
            if count % 100 == 0:
                print('On edge %i of %i' % (count, len(edge_ids)))

    def traverse_nodes(self):
        node_ids = self.graph.database.get_all_node_ids()
        count = 0
        for nid in node_ids:
            count += 1
            self.graph.create_node(nid[0])
            if count % 1000 == 0:
                print('On Node %i of %i' % (count, len(node_ids)))
