from query import Query
__author__ = 'nathir2'


if __name__ == "__main__":
    q = Query()
    node = q.get_node("2-Acetolactate Mutase")
    node = node[0][0]
    direct_rels = q.get_node_rels(node)
    direct_nodes = q.get_direct_nodes(node)
    print(direct_rels)
    print(direct_nodes)