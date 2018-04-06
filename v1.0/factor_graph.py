from state import NodeStateStore
from Pubsub import PubSub
from redis_broker import RedisBroker
from state import RedisNodeStateStore
from multiprocessing import Process, Manager, Array, current_process
from node_update_functions import ALGORITHM_TO_UPDATE_FUNCTIONS
from pagerank_converter import convert_adjacency_list_input_file_to_pagerank_factor_graph_and_register_with_pubsub
import time


decrypt = lambda x: float(x.decode("ascii")) if type(x) == bytes else x 




class FactorGraph:
    def __init__(self, path_to_input_file=None, config={}):
        self.factor_nodes = list() 
        self.variable_nodes = list() 
        self.edges = list() 
        self.pubsub = PubSub(config['pubsub_choice'])

        self.config = config
        self.algorithm = config["algorithm"]
        self.path_to_input_file = path_to_input_file
        self.initialize_nodes_and_edges() 
        self.pubsub.start()
        time.sleep(0.1) #why sleep here

    def initialize_nodes_and_edges(self): 
        """
        populates nodes and edges in FactorGraph
        currently manually makes nodes but should read input file
        """

        algo_to_use = "None"

        if self.algorithm == "page_rank": # this assume reading from the file which specifies factor graph structure
            algo_to_use = "page_rank_fake"
        elif self.algorithm == "max_product":
            algo_to_use = "max_product"

        update_var_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[algo_to_use]["update_var"]
        wrapper_var_function = lambda incoming_message: message_pass_wrapper(incoming_message, update_var_function)
        update_fac_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[algo_to_use]["update_fac"]
        wrapper_fac_function = lambda incoming_message: message_pass_wrapper(incoming_message, update_fac_function)

        self = convert_adjacency_list_input_file_to_pagerank_factor_graph_and_register_with_pubsub(self.path_to_input_file, self.pubsub, wrapper_var_function, wrapper_fac_function, self)
        




#document format of incoming_message??
#this is the problematic function
def message_pass_wrapper(incoming_message, input_function):
    node_id = incoming_message["channel"].decode("ascii").split("_")[1]
    updated_node_cache = update_node_cache(incoming_message, node_id) # I'm not sure why making new function for this

    stop_countdown = NodeStateStore("redis").fetch_node(node_id,"stop_countdown")

    if stop_countdown > 0:
        for to_node_id in list(updated_node_cache.keys()):
            send_to_channel_name = node_id + "_" + to_node_id
            new_outgoing_message = compute_outgoing_message(input_function,updated_node_cache,node_id,to_node_id)
            propagate_message(send_to_channel_name, new_outgoing_message)
            NodeStateStore("redis").countdown_by_one(node_id)


 


def convert_adjacency_list_input_file_to_pagerank_factor_graph_and_register_with_pubsub(path_to_input_file, pubsub, wrapper_var_function, wrapper_fac_function, factor_graph):
    (adjacency_dict_var,adjacency_dict_fac) = read_file_factor_graph(path_to_input_file) #{1:[2,3]}
    num_node = len(adjacency_dict_var)

    for variable_id in adjacency_dict_var:
        initial_messages_var = dict(adjacency_dict_var[variable_id])
        print(initial_messages_var)
        node_data = len(adjacency_dict_var[variable_id])-1
        variable_node = Node(variable_id,"variable",wrapper_var_function,initial_messages_var,node_data,pubsub)
        factor_graph.variable_nodes.append(variable_node)

    for factor_id in adjacency_dict_fac:
        initial_messages_fac = dict(adjacency_dict_fac[factor_id])
        node_data = 0
        factor_node = Node(factor_id,"factor",wrapper_fac_function,initial_messages_fac,node_data,pubsub)
        factor_graph.factor_nodes.append(factor_node)

    for variable_id in adjacency_dict_var:
        for (factor_id,initial_message) in adjacency_dict_var[variable_id]:
            channel_name = variable_id + "_" + factor_id
            edge = Edge(variable_id,factor_id, channel_name, pubsub)
            factor_graph.edges.append(edge)

    for factor_id in adjacency_dict_fac:
        for (variable_id,initial_message) in adjacency_dict_fac[factor_id]:
            channel_name = factor_id + "_" + variable_id
            edge = Edge(factor_id,variable_id, channel_name, pubsub)
            factor_graph.edges.append(edge)

    return factor_graph


def read_file_factor_graph(path_to_input_file): 
    adjacency_dict_var = dict() #key: variable index, value: list of factor index
    adjacency_dict_fac = dict()
    with open(path_to_input_file) as f:
        all_lines = f.readlines()
        for line in all_lines:
            [x,y,initial_incoming_message] = line.split()
            initial_incoming_message = float(initial_incoming_message)

            if y[0]=="v":
                add_to_adjacency_dict = adjacency_dict_var
            elif y[0]=="f":
                add_to_adjacency_dict = adjacency_dict_fac

            if y in add_to_adjacency_dict:
                add_to_adjacency_dict[y].append((x,initial_incoming_message))
            else:
                add_to_adjacency_dict[y] = [(x,initial_incoming_message)]

    return (adjacency_dict_var,adjacency_dict_fac)




    

def update_node_cache(incoming_message, node_id):
    updated_node_cache = NodeStateStore("redis").update_node(incoming_message, node_id)
    return updated_node_cache

def compute_outgoing_message(input_function,updated_node_cache,from_node_id,to_node_id):
    print("im here")
    node_data = NodeStateStore("redis").fetch_node(from_node_id,"node_data")
    print("node data ", node_data)
    new_outgoing_message = input_function(node_data, updated_node_cache,from_node_id,to_node_id)
    return new_outgoing_message

def propagate_message(channel_name, new_outgoing_message):
    redis = RedisBroker()
    redis.publish(channel_name,new_outgoing_message)


class FactorGraphService:
    def __init__(self):
        pass

    def create(self, path_to_input_file, config):
        factor_graph = FactorGraph(path_to_input_file, config)
        return factor_graph

    def run(self, factor_graph):
        #answer_dictionary = dict()
        #        redis = RedisBroker()

        #return answer_dictionary

        #pseudo
        print("hib")
        for variable_node in factor_graph.variable_nodes:
            propagate_message('v0_f0', 'hello')


class Edge:
    def __init__(self, from_node_id, to_node_id, edge_id, pubsub):
        self.pubsub = pubsub
        self.pubsub.register_channel(edge_id)
        self.pubsub.register_subscription(to_node_id, edge_id)


class Node:
    def __init__(self,node_id,node_type,node_function,initial_node_message_cache,node_data,pubsub):
        self.pubsub = pubsub
        self.state_store = NodeStateStore("redis")
        self.state_store.create_node_state(node_id,initial_node_message_cache,node_type,node_data)
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id,node_function)





    

if __name__ == "__main__":
    config = {
    "algorithm": "max_product",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
    }

    path_to_input_file = "test_input.txt"
    try_fg = FactorGraph(path_to_input_file, config)
    service = FactorGraphService()
    service.run(try_fg)


def first_try():
    config = {
    "algorithm": "max_product",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
    }

    path_to_input_file = "test_input.txt"
    try_fg = FactorGraph(path_to_input_file, config)
    service = FactorGraphService()
    service.run(try_fg)




