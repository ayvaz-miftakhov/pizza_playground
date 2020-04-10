import db_resturcture, layers_parse
from py2neo import Graph, Relationship
import json

graph = Graph("bolt://neo4j:1@localhost:7687")

db_resturcture.restructure_relations(graph)
db_resturcture.restructure_nodes(graph)

with open('layers.json') as json_file:
    layers_data = json.load(json_file)
layers_parse.add_layer(graph, layers_data)

layers_info = (layers_parse.get_layers_info(graph))
with open('layers_output.json', 'w') as outfile:
    json.dump(layers_info, outfile, indent=2)
