from query import Query
__author__ = 'nathir2'


if __name__ == "__main__":
    q = Query()
    node = q.get_node("2-Acetolactate Mutase")
    node = node[0][0]
    results = q.get_rels_from_node(node)
    print(results)