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
        pass

    def write_to_file(self):
        pass

    def convert_to_factor_graph_and_write_file(self):
        pass

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

    def write_as_factor_graph(self, observations, file_name):
        factor_node_initial_messages = {}
        factor_graph_vertices = {}
        with open(file_name, 'w+') as f:
            f.write('Edges\n')
            for node_id, probability in self.nodes.items():
                if self.__get_node_type(node_id) is 'hidden':
                    variable_node_id = node_id.replace('x', 'v')
                    if self.__is_initial_hidden_node(node_id):
                        initial_message = None #self.initial_variable_probability
                        factor_node_id = None
                        factor_graph_vertices[variable_node_id] = \
                        self.initial_variable_probability
                    else:
                        initial_message = None
                        factor_node_id = node_id.replace('x', 'f') + \
                        str(int(node_id[1:]) - 1)
                        factor_graph_vertices[variable_node_id] = np.ones(len(self.hidden_alphabet))
                        
                    factor_node_initial_messages[node_id] = initial_message
                    if factor_node_id is not None:
                        f.write(variable_node_id + ' ' + factor_node_id + \
                                ' ' + str(initial_message.tolist()).replace(' ','')+ '\n')
                        f.write(factor_node_id + ' ' + variable_node_id + \
                                ' ' + \
                                str(np.ones(len(self.hidden_alphabet)).tolist()).replace(' ', '')+ '\n')
                        previous_variable_node_id = \
                        self.__get_previous_hidden_node_id(node_id)
                        previous_initial_message = \
                        factor_node_initial_messages[previous_variable_node_id]
                        f.write(previous_variable_node_id.replace('x', 'v') + ' ' + factor_node_id + ' ' +\
                                ' ' +\
                                str(previous_initial_message.tolist()).replace(' ', '')+ '\n')
                        f.write(factor_node_id + ' ' +\
                                previous_variable_node_id.replace('x', 'v') + \
                                ' ' + \
                                str(np.ones(len(self.hidden_alphabet)).tolist()).replace(' ', '')+ '\n')
                        factor_graph_vertices[factor_node_id] = \
                        self.hidden_transition_probability_matrix
                else:
                    observation = observations[node_id]
                    observation_value_index = self.sample_alphabet.index(int(observation))
                    initial_message = np.zeros(len(self.sample_alphabet))
                    initial_message[observation_value_index] = 1

                    factor_node_id = node_id.replace('y', 'f') + \
                    str(int(node_id[1:]))
                    variable_node_id = node_id.replace('y', 'v0')

                    f.write(variable_node_id + ' ' + factor_node_id + \
                            ' ' + str(initial_message.tolist()).replace(' ', '') + '\n')
                    f.write(factor_node_id + ' ' + variable_node_id + \
                            ' ' + \
                            str(np.ones(len(self.hidden_alphabet)).tolist()).replace(' ', '')+ '\n')
                    hidden_variable_node_id = \
                    self.__get_hidden_node_id_for_sample_node(node_id).replace('x',
                            'v')
                    hidden_initial_message = None
                    f.write(hidden_variable_node_id + ' ' + factor_node_id + \
                            ' ' + str(hidden_initial_message).replace(' ', '')+ '\n')
                    f.write(factor_node_id + ' ' + hidden_variable_node_id + \
                            ' ' + \
                            str(np.ones(len(self.hidden_alphabet)).tolist()).replace(' ', '')+ '\n')
                    factor_graph_vertices[variable_node_id] = None 
                    factor_graph_vertices[factor_node_id] = \
                    self.sample_probability
            f.write('Vertices\n')
            for node_id, probability in factor_graph_vertices.items():
                if probability is not None:
                    probability = probability.tolist()
                f.write(node_id + ' ' + str(probability).replace(' ', '') + '\n')

#            for node_id, probability in self.nodes.items():

#                    observation_conditional_probability = \
#                    self.sample_probability[observation_value_index]

    def convert_to_factor_graph_old(self, observations, file_name):
        factor_node_initial_messages = {}
        with open(file_name, 'w+') as f:
            for node_id, probability in self.nodes.items():
                if self.__get_node_type(node_id) is 'hidden' or 'x' in node_id:
                    if self.__is_initial_hidden_node(node_id):
                        initial_message = self.initial_variable_probability
                        factor_node_id = None
                    else:
                        initial_message = np.ones(len(self.hidden_alphabet))
                        factor_node_id = node_id.replace('x', 'f') + \
                        str(int(node_id[1:]) - 1)
                    factor_node_initial_messages[node_id] = initial_message
                    observation_id = node_id.replace('x', 'y')
                    observation = observations[observation_id]
                    observation_value_index = self.sample_alphabet.index(int(observation))
                    observation_conditional_probability = \
                    self.sample_probability[observation_value_index]
                    ## get sample observation
                    initial_message *= observation_conditional_probability
                    variable_node_id = node_id.replace('x', 'v')
                    if factor_node_id is not None:
                        f.write(variable_node_id + ' ' + factor_node_id + \
                                str(initial_message.tolist()) + '\n')
                        f.write(factor_node_id + ' ' + variable_node_id + \
                                str(np.ones(len(self.hidden_alphabet)).tolist()) + '\n')
                        previous_variable_node_id = \
                        self.__get_previous_hidden_node_id(node_id)
                        previous_initial_message = \
                        factor_node_initial_messages[previous_variable_node_id]
                        f.write(previous_variable_node_id + ' ' + factor_node_id + \
                                str(previous_initial_message.tolist()) + '\n')
                        f.write(factor_node_id + ' ' + previous_variable_node_id + \
                                str(np.ones(len(self.hidden_alphabet)).tolist()) + '\n')

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

