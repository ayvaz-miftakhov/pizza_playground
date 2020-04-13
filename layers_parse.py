from py2neo import Node, Relationship, NodeMatcher


def add_layer(graph, layers_dict):
    for layer in layers_dict['layers']:
        layer_node = Node("Layer", name=layer['name'])
        for element in layer['elements']:
            layer_chain = Relationship(layer_node, "CONTAINS", graph.nodes.match("Element", name=element).first())
            graph.create(layer_chain)


def get_layers_names(graph):
    layers_dict = {}

    for layer_node in graph.nodes.match("Layer"):
        layers_dict[layer_node.identity] = layer_node["name"]

    return layers_dict


def get_layers_info(graph, *id_list):
    layers_dict = {"layers": []}

    if len(id_list) == 0:
        layers_list = graph.nodes.match("Layer")
    else:
        layers_list = []
        matcher = NodeMatcher(graph)
        for layer_id in id_list:
            layers_list.append(matcher.get(layer_id))

    for layer_node in layers_list:
        layer_info = {"name": layer_node["name"], "id": layer_node.identity, "elements": []}
        layer_rels = graph.relationships.match((layer_node, None), "CONTAINS")

        indexes = []  # KOCTbI/\b
        for node_rel in layer_rels.__iter__():
            indexes.append(node_rel.nodes[1].identity)

        for rel in layer_rels.__iter__():
            cur_node = rel.nodes[1]
            elem_info = {"id": cur_node.identity, "name": cur_node["name"], "relations": []}

            for cur_node_rel in graph.relationships.match((cur_node, None), None):
                neighbour_node = cur_node_rel.nodes[1]
                if neighbour_node.identity in indexes:
                    elem_info["relations"].append({"rel_type": cur_node_rel["name"],
                                                   "id": neighbour_node.identity, "name": neighbour_node["name"]})

            layer_info["elements"].append(elem_info)

        layers_dict["layers"].append(layer_info)

    return layers_dict
