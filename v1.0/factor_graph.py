from Pubsub import PubSub
from state import RedisNodeStateStore
from multiprocessing import Process, Manager, Array, current_process
from node_update_functions import ALGORITHM_TO_UPDATE_FUNCTIONS
from redis import Redis
from redis_callback_class import *
from reader import FactorGraphReader
from node import Node
from edge import Edge
import time
import pdb


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
        time.sleep(0.1)

    def initialize_nodes_and_edges(self): 
        """
        populates nodes and edges in FactorGraph
        currently manually makes nodes but should read input file
        """

        update_var_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[self.algorithm]["update_var"]
        wrapper_var_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_var_function, self.pubsub)
        update_fac_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[self.algorithm]["update_fac"]
        wrapper_fac_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_fac_function, self.pubsub)

        self = FactorGraphReader.register_pubsub_from_pagerank_adjacency_list(self.path_to_input_file, self.pubsub, wrapper_var_function, wrapper_fac_function, self)
    
    def run(self):
        for node in self.variable_nodes:
            node.receive_messages_from_neighbors()



if __name__ == "__main__":
    r = Redis()
    r.flushall()

    config = {
        "algorithm": "page_rank",
        "pubsub_choice": "redis",
        "synchronous": "asynchronous"
    }

    path_to_input_file = "examples/pagerank_graph_adjaceny_list_example.txt"

    # config = {
    #     "algorithm": "try_pickle",
    #     "pubsub_choice": "redis",
    #     "synchronous": "asynchronous"
    # }
    # path_to_input_file = "examples/try_pickle_fg_input.txt"

    try_fg = FactorGraph(path_to_input_file, config)
    try_fg.run()
    time.sleep(20)
    print(try_fg.get_result())


