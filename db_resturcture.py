from py2neo import Relationship


def restructure_relations(graph):
    for rel_node in graph.nodes.match("relationships"):
        open_node = graph.relationships.match((None, rel_node), None)
        close_node = graph.relationships.match((rel_node, None), None)
        graph.create(Relationship(open_node.first().nodes[0], rel_node["class"], close_node.first().nodes[1]))
        graph.delete(rel_node)


def restructure_nodes(graph):
    for node in graph.nodes.match("elements"):
        node.remove_label("elements")
        node.add_label("Element")
        node.add_label(node["class"])
        del(node["checksum"], node["class"], node["documentation"], node["id"], node["version"])
        node["name"] = node["name"].strip()
        graph.push(node)
