from factor_graph import FactorGraph, FactorGraphService, Node
from pubsub import Publisher, Channel, Subscriber, PubSub


factor_graph = FactorGraph()

variable_nodes = []
factor_nodes = []
one_variable_node = Node(0, lambda x, y: x+y)
one_factor_node = Node(1, lambda x, y: x-y)

variable_nodes.append(one_variable_node)
factor_nodes.append(one_factor_node)


incoming_message = 1

for i in range(10):
	if i%2==0:
		for v in variable_nodes:
			v.message_pass(incoming_message)
	else:
		for f in factor_nodes:
			f.message_pass(incoming_message)

print("apache tsunami complete")