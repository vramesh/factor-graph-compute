from Pubsub import PubSub
from state import RedisNodeStateStore
from multiprocessing import Process, Manager, Array, current_process
from node_update_functions import ALGORITHM_TO_UPDATE_FUNCTIONS
from redis import Redis
from redis_callback_class import *
from reader import FactorGraphReader
from node import Node
from edge import Edge
from input_to_fg_converter import convert_to_page_rank_factor_graph_file
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
        
        '''
        if (self.algorithm == "page_rank"):
            convert_to_page_rank_factor_graph_file(self.path_to_input_file,self.path_to_factor_graph_file)
            self = FactorGraphReader.register_pubsub_from_pagerank_adjacency_list(self.path_to_factor_graph_file, self.pubsub, wrapper_var_function, wrapper_fac_function, self)
        elif (self.algorithm == "try_pickle"):
            self.path_to_factor_graph_file = "examples/try_pickle_fg_input.txt"
            self = FactorGraphReader.register_pubsub_from_pagerank_adjacency_list(self.path_to_factor_graph_file, self.pubsub, wrapper_var_function, wrapper_fac_function, self)
        
        else:
            print("Haven't implemented this algorithm yet")
        '''


    def run(self):
        for node in self.variable_nodes:
            node.receive_messages_from_neighbors()

    def get_result(self):
        results = list()
        for node in self.variable_nodes:
            results.append(node.get_current_cached())
        return results

    def print_solution(self):
        for node in self.variable_nodes:
            print(node.node_id, ": ", node.get_final_state(self.algorithm))




if __name__ == "__main__":
    r = Redis()
    r.flushall()


    config = {
        "algorithm": "sum_product",
        "pubsub_choice": "redis",
        "synchronous": "asynchronous"
    }
    path_to_input_file = "examples/hmm_simple_factor_graph.txt"

    try_fg = FactorGraph(path_to_input_file, config)
    try_fg.run()
    time.sleep(20)
    print(try_fg.get_result())


