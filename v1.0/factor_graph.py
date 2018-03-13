from state import NodeStateStore
from Pubsub import PubSub
from redis_broker import RedisBroker
from state import RedisNodeStateStore
from multiprocessing import Process, Manager, Array, current_process
import time

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": lambda state, messages, sender_id, recipient_id: messages[sender_id]/state if sender_id!=recipient_id else 0 ,
        "update_fac": lambda state, messages, sender_id, recipient_id: sum([messages.values()]) - messages[sender_id] if sender_id == recipient_id else 0
    }
}


toy_config = \
{
    "algorithm": "hello_world",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
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

        #logic for updateing update_function_custom argument
        if self.algorithm == "hello_world":
            simple_message_pass = lambda incoming_message: message_pass_wrapper(incoming_message, lambda x: print("hello" + str(incoming_message) ))
            node_1 = Node(1, "variable", simple_message_pass, "hello", self.pubsub)
            node_2 = Node(2, "factor", simple_message_pass, "goodbye", self.pubsub)
            edge = Edge(1, 2, "first_edge_bois", self.pubsub)
            self.variable_nodes.append(node_1)
            self.factor_nodes.append(node_2)
            self.edges.append(edge)

        if self.algorithm == "page_rank": # this assume reading from the file which specifies factor graph structure
            update_var_function  = ALGORITHM_TO_UPDATE_FUNCTIONS["page_rank"]["update_var"]
            wrapper_var_function = lambda incoming_message: message_pass_wrapper(incoming_message, update_var_function)
            update_fac_function  = ALGORITHM_TO_UPDATE_FUNCTIONS["page_rank"]["update_fac"]
            wrapper_fac_function = lambda incoming_message: message_pass_wrapper(incoming_message, update_fac_function)
            (adjacency_dict_var,adjacency_dict_fac) = read_file_factor_graph(self.path_to_input_file) #{1:[2,3]}
            num_node = len(adjacency_dict_var)

            for variable_index in adjacency_dict_var:
                variable_name = "v" + str(variable_index)
                initial_messages_var = dict([(x,0) for x in adjacency_dict_var[variable_index]])
                initial_messages_var[variable_index] = 1/num_node
                node_data = len(adjacency_dict_var[variable_index])
                variable_node = Node(variable_name,"variable",wrapper_var_function,initial_messages_var, node_data, self.pubsub)
                self.variable_nodes.append(variable_node)

            for factor_index in adjacency_dict_fac:
                factor_name = "f" + str(factor_index)
                initial_messages_fac = dict([(x,0) for x in adjacency_dict_fac[factor_index]])
                initial_messages_fac[factor_index] = 0
                node_data = None
                factor_node = Node(factor_name,"factor",wrapper_fac_function,initial_messages_fac, node_data, self.pubsub)
                self.factor_nodes.append(factor_node)

            for variable_index in adjacency_dict_var:
                for factor_index in adjacency_dict_var[variable_index]:
                    variable_name = "v" + str(variable_index)
                    factor_name = "f" + str(factor_index)
                    channel_name = "v"+str(variable_index)+"_f"+str(factor_index)
                    edge = Edge(variable_name,factor_name, channel_name, self.pubsub)
                    self.edges.append(edge)

            for factor_index in adjacency_dict_fac:
                for variable_index in adjacency_dict_fac[factor_index]:
                    variable_name = "v" + str(variable_index)
                    factor_name = "f" + str(factor_index)
                    channel_name = "f"+str(factor_index)+"_v"+str(variable_index)
                    edge = Edge(factor_name,variable_name, channel_name, self.pubsub)
                    self.edges.append(edge)



def read_file_factor_graph(path_to_input_file): 
    adjacency_dict_var = dict() #key: variable index, value: list of factor index
    adjacency_dict_fac = dict()
    with open(path_to_input_file) as f:
        all_lines = f.readlines()
        for line in all_lines:
            [x,y] = line.split()
            x = int(x)
            y = int(y)

            if x in adjacency_dict_var:
                adjacency_dict_var[x].append(y)
            else:
                adjacency_dict_var[x] = [y]

            if y in adjacency_dict_fac:
                adjacency_dict_fac[y].append(x)
            else:
                adjacency_dict_fac[y] = [x]

    return (adjacency_dict_var,adjacency_dict_fac)


#channel_name_convention: (type)index_(type)index
def message_pass_wrapper(incoming_message, input_function):
    node_id = current_process().name
    # from_node_type = 
    updated_node_cache = update_node_cache(incoming_message, node_id) #crash

    update_function = input_function
    for channel_name in all_channels:
        new_outgoing_message = self.__compute_outgoing_message(update_function, updated_state, channel_name)
        self.__propagate_message(new_outgoing_message, channel_name)
    

def update_node_cache(incoming_message, node_id):
    updated_node_cache = NodeStateStore("redis").update_node(incoming_message, node_id)
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
    def __init__(self, from_node_id, to_node_id, edge_id, pubsub):
        self.pubsub = pubsub
        self.pubsub.register_channel(edge_id)
        self.pubsub.register_subscription(to_node_id, edge_id)


class Node:
    def __init__(self, node_id, node_type, node_function, initial_node_message_cache, node_data, pubsub):
        self.pubsub = pubsub
        self.state_store = NodeStateStore("redis")
        self.state_store.create_node_state(node_id, initial_node_message_cache, node_type, node_data)
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id, node_function)




config = {
    "algorithm": "page_rank",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
}
# trying = FactorGraphService().create(None, config)
# time.sleep(1)
# FactorGraphService().run(trying)

# path_to_input_file = "input.txt"
# try_fg = FactorGraph(path_to_input_file,config)






'''
def __update_state(self, incoming_message):
    new_full_state = self.node_message_cache.update(incoming_message, self.node_id)
    return new_full_state

def __compute_outgoing_message(self, updated_state, channel_name):
    new_outgoing_message = ""  # need callback function here, which in turn need permanent state, all current messages, so node_message_cache need to send it here?
    return new_outgoing_message

def __propagate_message(self, new_outgoing_message):
    self.publisher.publish(new_outgoing_message)
'''
