from Pubsub import PubSub
from reader import FactorGraphReader
import time


class FactorGraph:
    def __init__(self, path_to_input_file=None, config={}):
        self.factor_nodes = list() 
        self.variable_nodes = list() 
        self.stop_node = None
        self.edges = list() 
        self.pubsub = PubSub(config['pubsub_choice'])
        self.config = config
        self.algorithm = config["algorithm"]
        self.path_to_input_file = path_to_input_file
        self.number_of_iter = config["number_of_iter"]
        self.time_till_stop = config["time_till_stop"]
        self.initialize_nodes_and_edges() 
        self.pubsub.start()
        time.sleep(0.1)

    def initialize_nodes_and_edges(self): 
        """
        populates nodes and edges in FactorGraph
        currently manually makes nodes but should read input file
        """
        self = FactorGraphReader.register_pubsub_from_factor_graph_file(self)


    def run(self):
        for node in self.variable_nodes:
            node.send_initial_messages()
        stop_signal = self.stop_node.get_stop_signal()
        if stop_signal:
            return True

    def get_result(self, output_file):
        # results = list()
        # for node in self.variable_nodes:
        #     results.append(node.get_current_cached())
        with open(output_file,"w") as f:
            f.write("Most Recent Message Cached\n")
            f.write("Variable Nodes\n")
            for variable_node in self.variable_nodes:
                f.write(variable_node.get_id())
                f.write(" : ")
                f.write(str(variable_node.get_current_cached()))
                f.write("\n")
            f.write("Factor Nodes\n")
            for factor_node in self.factor_nodes:
                f.write(factor_node.get_id())
                f.write(" : ")
                f.write(str(factor_node.get_current_cached()))
                f.write("\n")
        return None

    def print_solution(self):
        print("print results")
        for node in self.variable_nodes:
            if node.node_id[1]!='0':
                print(node.node_id, ": ", node.get_final_state(self.algorithm))


