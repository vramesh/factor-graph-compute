import numpy as np
import time
import pdb


class GraphicalModel:
    def __init__(self, path_to_input_file=None, config={}):
        self.nodes = {} 
        self.edges = {} 
        self.config = config
        if path_to_input_file:
            self.path_to_input_file = path_to_input_file
            self.initialize_nodes_and_edges() 

    def initialize_nodes_and_edges(self): 
        """
        populates nodes and edges in GraphicalModel 
        currently manually makes nodes but should read input file
        """

#        self = FactorGraphReader.register_pubsub_from_pagerank_adjacency_list(self.path_to_input_file, self.pubsub, wrapper_var_function, wrapper_fac_function, self)
        
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

    def write_to_file(self):
        pass

    def convert_to_factor_graph_and_write_file(self):
        for edge, probability in self.edges.items():
            ## create factor node for edge
            ## create variable node for sink node 
            ## create variable-factor edge for sink node 
            ## create variable node for source node 
            ## create variable-factor edge for source node 

        for node_probability in self.nodes.items():
            ## create variable node

class HiddenMarkovModel(GraphicalModel):
    def __init__(self, number_of_variables, hidden_transition_probability_matrix,
            sample_probability, initial_variable_probability, hidden_alphabet,
            sample_alphabet):
        self.number_of_variables = number_of_variables
        self.hidden_transition_probability_matrix = \
        hidden_transition_probability_matrix
        self.sample_probability = sample_probability
        self.initial_variable_probability = initial_variable_probability
        self.hidden_alphabet = hidden_alphabet
        self.sample_alphabet = sample_alphabet
        self.nodes = {}
        self.edges = {} 
        self.__initialize_graphical_model()

    def generate_observations(self):
        return {node_id: self.__generate_observation_sample(node_id) for
                node_id, probability in self.nodes.items() if
                self.__get_node_type(node_id) is 'sample'}

    '''
    def convert_to_factor_graph(self):
        factor_edges = {}
        factor_nodes = {}
        for node_id, probability in self.nodes.items():
            if self.__get_node_type(node_id) is 'hidden':
                self.__create_factor_graph_variable_node()
                if not self.__is_initial_hidden_node(self, node_id):
                    self.__create_factor_graph_factor_node()
                    self.__create_factor_graph_edges()
    '''

    def __generate_observation_sample(self, sample_variable_node_id):
        sample_probability = self.nodes[sample_variable_node_id]
        return np.random.choice(self.sample_alphabet,
                size=1,p=sample_probability.tolist())[0]
                    

    def __initialize_graphical_model(self):
        [self.__add_variable(variable) for variable in
                range(self.number_of_variables)]

    def __add_variable(self, variable_id):
        sample_variable_id = 'y'+str(variable_id)
        self.__add_hidden_variable_node(variable_id)
        self.__add_sample_variable_node(sample_variable_id)

    def __add_hidden_variable_node(self, variable_id):
        hidden_variable_node_id = 'x'+str(variable_id)
        self.__create_hidden_variable_node(hidden_variable_node_id)
        self.__create_hidden_variable_incoming_transition_edge(hidden_variable_node_id)

    def __create_hidden_variable_node(self, hidden_variable_node_id):
        if self.__is_initial_hidden_node(hidden_variable_node_id):
            self.nodes[hidden_variable_node_id] = self.initial_variable_probability
        else:
            previous_hidden_node_id = \
            self.__get_previous_hidden_node_id(hidden_variable_node_id)

            previous_hidden_node_probability = \
            self.nodes[previous_hidden_node_id]

            self.nodes[hidden_variable_node_id] = \
            np.dot(self.hidden_transition_probability_matrix,
                    self.initial_variable_probability)
        

    def __create_hidden_variable_incoming_transition_edge(self,
            hidden_variable_node_id):
        if not self.__is_initial_hidden_node(hidden_variable_node_id):
            previous_hidden_node_id = \
            self.__get_previous_hidden_node_id(hidden_variable_node_id)
            edge_id = self.__get_edge_id(previous_hidden_node_id,
                    hidden_variable_node_id) 
            self.edges[edge_id] = self.hidden_transition_probability_matrix

    def __add_sample_variable_node(self, sample_variable_id):
        self.__create_sample_variable_node(sample_variable_id)
        self.__create_sample_variable_incoming_transition_edge(sample_variable_id)

    def __create_sample_variable_node(self, sample_variable_id):
        hidden_node_id = \
        self.__get_hidden_node_id_for_sample_node(sample_variable_id)
        hidden_node_probability = self.nodes[hidden_node_id]
        self.nodes[sample_variable_id] = np.dot(self.sample_probability,
                hidden_node_probability) 

    def __create_sample_variable_incoming_transition_edge(self, sample_variable_id):
        hidden_node_id = \
        self.__get_hidden_node_id_for_sample_node(sample_variable_id)
        edge_id = self.__get_edge_id(hidden_node_id, sample_variable_id) 
        self.edges[edge_id] = self.sample_probability 

    def __is_initial_hidden_node(self, variable_id):
        return True if 'x0' == variable_id else False

    def __get_previous_hidden_node_id(self, hidden_variable_id):
        return None if self.__is_initial_hidden_node(hidden_variable_id)\
        else'x' + str(int(hidden_variable_id[1:]) - 1)

    def __get_hidden_node_id_for_sample_node(self, sample_node_id):
        return sample_node_id.replace('y', 'x')

    def __get_edge_id(self, source_node_id, sink_node_id):
        return 'e' + source_node_id[1:] + '_' + sink_node_id[1:]

    def __get_node_type(self, variable_node_id):
        return 'sample' if 'y' in variable_node_id else 'hidden'

