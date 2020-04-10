from py2neo import Node, Relationship


def add_layer(graph, layers_dict):
    for layer in layers_dict['layers']:
        layer_node = Node("Layer", name=layer['name'])
        for element in layer['elements']:
            layer_chain = Relationship(layer_node, "CONTAINS", graph.nodes.match("Element", name=element).first())
            graph.create(layer_chain)


def get_layers_info(graph):
    layers_dict = {"layers": []}

    for layer_node in graph.nodes.match("Layer"):
        layer_info = {"name": layer_node["name"], "id": layer_node.identity, "elements": []}
        layer_rel = graph.relationships.match((layer_node, None), "CONTAINS")
        for node_rel in layer_rel.__iter__():
            elem_info = {"id": node_rel.nodes[1].identity, "name": node_rel.nodes[1]["name"]}
            layer_info["elements"].append(elem_info)
        layers_dict["layers"].append(layer_info)

    return layers_dict
