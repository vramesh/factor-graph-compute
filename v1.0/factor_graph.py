from pubsub import PubSub
from state import StateStore, NodeState
from pubsub import Publisher, Subscriber, Channel, PubSub

class FactorGraph:
	def __init__(self):
		self.factor_nodes = list() #list of Node objects
		self.variable_nodes = list() #list of Node objects
		self.edges = list() #list of Edge objects



class FactorGraphService:
	def __init__(self):
		pass

	def create(self, path_to_file):
		factor_graph = FactorGraph()
		return factor_graph

	def run(self, factor_graph):
		answer_dictionary = dict()
		return answer_dictionary


class Edge:
	def __init__(self, edge_id):
		self.channel = Channel()
		self.channel.register()


class Node:
	def __init__(self, node_id, node_function):
		self.node_id = node_id
		self.publisher = Publisher(node_id)
		self.subscriber = Subscriber(node_id)
		self.publisher.register()
		self.subscriber.register(node_function)

	def message_pass(self, incoming_message): 
		#main callback for pubsub
		#pubsubs handles active listening
		updated_state = self.update_state(incoming_message)
		new_outgoing_message = self.compute_outgoing_message(updated_state)
		self.propagate_message(new_outgoing_message)

	def update_state(self, incoming_message):
		'''
		node_state = StateStore[self.node_id]
		new_full_state = node_state.update(incoming_message, self.node_id)
		return new_full_state
		'''
		return incoming_message

	def compute_outgoing_message(self, some_state):
		new_outgoing_message = "" 
		return new_outgoing_message

	def propagate_message(self, new_outgoing_message):
		self.publisher.publish()

		