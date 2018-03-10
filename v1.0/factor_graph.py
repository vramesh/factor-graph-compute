from state import StateStore, NodeState
from pubsub import PubSub
from redis_broker import RedisBroker
import time

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": lambda state, messages, sender_index, recipient_index: messages[sender_index]/state if sender_index!=recipient_index else 0 ,
        "update_fac": lambda state, messages, sender_index, recipient_index: sum([messages.values()]) - messages[sender_index] if sender_index == recipient_index else 0
    }
}

class FactorGraph:
    def __init__(self, path_to_input_file, config):
        self.factor_nodes = list() 
        self.variable_nodes = list() 
        self.edges = list() 
        self.pubsub = PubSub(config['pubsub_choice'])

        self.config = config
        self.algorithm = config["algorithm"]
        self.path_to_input_file = path_to_input_file

        self.initialize_nodes_and_edges() 
        self.pubsub.start()

    def initialize_nodes_and_edges(self): 
        """
        populates nodes and edges in FactorGraph
        currently manually makes nodes but should read input file
        """
        node_1 = Node(1, "variable", message_pass, None, self.pubsub)
        node_2 = Node(2, "factor", lambda x: print("goodbye"), None, self.pubsub)
        edge = Edge(1, 2, "first_edge_bois", self.pubsub)
        self.variable_nodes.append(node_1)
        self.factor_nodes.append(node_2)
        self.edges.append(edge)

def message_pass(incoming_message):
    print("hello")
    node_id = process.name()
    updated_node_cache = update_node_cache(incoming_message, node_id)
    for channel_name in all_channels:
        new_outgoing_message = self.__compute_outgoing_message(updated_state, channel_name)
        self.__propagate_message(new_outgoing_message, channel_name)

def update_node_cache(incoming_message, node_id):
    node_cache_store = {1: 'blah', 2: 'hello'}
    updated_node_cache = node_cache_store.update(incoming_message, node_id)
    return updated_node_cache


class FactorGraphService:
    def __init__(self):
        pass

    def create(self, path_to_input_file, config):
        factor_graph = FactorGraph(path_to_input_file, config)
        return factor_graph

    def run(self, factor_graph):
        #answer_dictionary = dict()
        redis = RedisBroker()
        redis.publish("first_try","first_edge_bois")
        #return answer_dictionary


class Edge:
    def __init__(self, variable_node_id, factor_node_id, edge_id, pubsub):
        self.pubsub = pubsub
        self.pubsub.register_channel(edge_id)
        self.pubsub.register_subscription(variable_node_id, edge_id)
        self.pubsub.register_subscription(factor_node_id, edge_id)


class Node:
    def __init__(self, node_id, node_type, node_function, node_state, pubsub):
        self.node_id = node_id
        self.node_type = node_type
        self.node_state = node_state
        self.pubsub = pubsub
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id, node_function)


config = {
    "algorithm": "page_rank",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
}
trying = FactorGraphService().create(None, config)
time.sleep(1)
FactorGraphService().run(trying)


'''
def message_pass(self, incoming_message, all_channels): 
    #main callback for pubsub
    #pubsubs handles active listening
    updated_state = self.__update_state(incoming_message)
    for channel_name in all_channels:
        new_outgoing_message = self.__compute_outgoing_message(updated_state, channel_name)
        self.__propagate_message(new_outgoing_message, channel_name)

def __update_state(self, incoming_message):
    new_full_state = self.node_state.update(incoming_message, self.node_id)
    return new_full_state

def __compute_outgoing_message(self, updated_state, channel_name):
    new_outgoing_message = ""  # need callback function here, which in turn need permanent state, all current messages, so node_state need to send it here?
    return new_outgoing_message

def __propagate_message(self, new_outgoing_message):
    self.publisher.publish(new_outgoing_message)
'''
