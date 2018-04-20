from Pubsub import PubSub
from reader import FactorGraphReader
import time

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
        self = FactorGraphReader.make_factor_graph(self)
    
    def run(self):
        for node in self.variable_nodes:
            node.receive_messages_from_neighbors()


