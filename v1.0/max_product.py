import numpy as np
from collections import namedtuple
from sklearn.utils.extmath import cartesian
from scipy.stats import mode
from scipy.stats import itemfreq 
from attrdict import AttrDict
import pdb

def max_product_update_var(state, messages, sender_id, recipient_id):
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    outgoing_message = MaxProductVariableNode(sender_id,
            messages).update_edge_message(recipient_id)
    return outgoing_message

def max_product_update_fac(state, messages, sender_id, recipient_id):
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    outgoing_message = MaxProductFactorNode(sender_id,
            messages).update_edge_message(recipient_id)
    return outgoing_message 

class MaxProductNode():
    def __init__(self, node_id, incoming_messages):
        self.node_id = node_id 
        self.incoming_messages = [AttrDict({'message':
            np.array([1-neighbor_message, neighbor_message]), 'variable_cost': 1,
            'node_id': neighbor_id}) for neighbor_id, neighbor_message in
                incoming_messages.items()]

class MaxProductVariableNode(MaxProductNode):
    def __init__(self, variable_id, incoming_messages):
        MaxProductNode.__init__(self, variable_id, incoming_messages)

    def update_edge_message(self, neighbor_to_update):
        updated_edges = self.update_edges() 
        return [edge.message for edge in updated_edges if edge.node_id ==
                neighbor_to_update][0][1]
                

    def update_edges(self):
        edges = self.incoming_messages
        node_state = self.__node_state_from_edges(edges)
        new_edges = self.__edges_from_node_state(node_state, edges)
        return new_edges

    def update_edge_marginals(self, edges):
        marginal = self.__marginals_from_edges(edges)
        edges_with_marginals = self.__edges_from_marginals(marginal, edges)
        return edges_with_marginals 

    def __node_state_from_edges(self, edges):
        variable_cost_mean = edges[0].variable_cost
        variable_cost = variable_cost_mean#np.sign(variable_cost_mean)*np.random.exponential(np.abs(variable_cost_mean))
        message_product = np.array([1, np.exp(-1*variable_cost)])*self.__compute_message_product(edges)
        return self.__normalize_message(message_product)

    def __edges_from_node_state(self, node_state, edges):
        return [self.__compute_new_neighbor_message(node_state, edge) for edge in edges]

    def __marginals_from_edges(self, edges):
        unnormalized_marginal = self.__node_state_from_edges(edges)
        marginal = self.__normalize_message(unnormalized_marginal)
        return marginal 

    def __edges_from_marginals(self, marginal, edges):
        [setattr(edge, 'message', marginal) for edge in edges]
        return edges

    # Helper Methods
    def __compute_message_product(self, edges):
        edge_array = np.array([edge.message for edge in edges])
        message_product = np.prod(edge_array, axis=0) 
        return message_product

    def __compute_new_neighbor_message(self, message_product, edge):
    
        new_edge_message = \
        self.__normalize_message(np.nan_to_num(message_product/edge.message))

        edge.message = new_edge_message
        return edge

    def __normalize_message(self, message):
        noise = 1#np.array([0,1])*np.exp(np.random.normal())
        return message/float(message.sum()) if message.sum() > 0 else np.array([0.5, 0.5])*noise



class MaxProductFactorNode():
    def __init__(self, factor_id, incoming_messages):
        MaxProductNode.__init__(self, factor_id, incoming_messages)
        if '4' in factor_id:
            self.incoming_messages = [AttrDict({
                'message': np.array([1-neighbor_message, neighbor_message]), 
                'variable_cost': 1,
                'node_id': neighbor_id,
                'id': factor_id,
                'decimation_status': 0,
                'factor_function': (np.ones(len(incoming_messages)), np.array([1,1]))}) for neighbor_id, neighbor_message in
                    incoming_messages.items()]

        else:
            self.incoming_messages = [AttrDict({
                'message': np.array([1-neighbor_message, neighbor_message]), 
                'variable_cost': 1,
                'node_id': neighbor_id,
                'id': factor_id,
                'decimation_status': 0,
                'factor_function': (np.ones(len(incoming_messages)), np.array([0,1]))}) for neighbor_id, neighbor_message in
                    incoming_messages.items()]

    def update_edge_message(self, neighbor_to_update):
        updated_edges = self.update_edges() 
        return [edge.message for edge in updated_edges if edge.node_id ==
                neighbor_to_update][0][1]

    def update_edges(self):
        edges = self.incoming_messages
        node_state = self.__node_state_from_edges(edges)
        new_edges = self.__edges_from_node_state(node_state, edges)
        return new_edges

    def __perturb_edge_message(self, edge):
        edge.message *= np.array([1, np.exp(-1*edge.variable_cost)])
        edge.message = self.__normalize(edge.message)
        return edge

    def compute_constraint_score(self, edges):
        factor_function_params = edges[0].factor_function
        factor_coeffs, factor_bounds = factor_function_params 

        marginal_values_vector = np.array([np.argmax(edge.message) for edge in
            sorted(edges, key=lambda edge: edge.node_id)])

        factor_function_value = np.inner(factor_coeffs,
                marginal_values_vector)

        constraint_score = 1
        if factor_bounds[0]: 
            if factor_bounds[0] <= factor_function_value:
                upper_constraint_score = 1 
            else:
                upper_constraint_score = 0 
        else:
            upper_constraint_score = 1

        if factor_bounds[1]: 
            if factor_bounds[1] >= factor_function_value:
                lower_constraint_score = 1 
            else:
                lower_constraint_score = 0  
        else:
            lower_constraint_score = 1

        constraint_score = 1 - upper_constraint_score*lower_constraint_score
        return constraint_score

    def __node_state_from_edges(self, edges):
        neighbor_messages = sorted(edges, key=lambda edge: edge.node_id)

        samples = self.__generate_sample_vectors(neighbor_messages)

        factor_coeffs, factor_bounds = edges[0].factor_function

        factor_function = lambda values: 1 if (factor_bounds[0] <=
                np.inner(factor_coeffs, values) <= (factor_bounds[1] or np.inf)) else 0

        return AttrDict({'samples': samples, 'factor_function':
            factor_function})
            

    def __edges_from_node_state(self, node_state, edges):
        to_decimate = False

        neighbor_messages = sorted(edges, key=lambda edge: edge.node_id)
        new_messages = [self.__update_factor_edge(edge, index, node_state.samples,
            node_state.factor_function, to_decimate) for index, edge in
            enumerate(neighbor_messages)]
            
        return new_messages

    ## Helper Methods

    def __generate_sample_vectors(self, sorted_edges):
        num_samples = 1000
        sample_vectors = np.array([np.random.choice([0,1], num_samples,
            p=edge.message.tolist()) for edge in sorted_edges]).T

        return sample_vectors

    def __update_factor_edge(self, edge, index, samples, factor_function,
            to_decimate=None):

        decimation_status = edge.decimation_status
        edge_id = edge.id
        current_message = edge.message


        message_update = self.__compute_new_message_from_sample_vectors(index, samples,
                factor_function)
        
        decimation_update = decimation_status
        edge.message = message_update
        return edge

    def __compute_new_message_from_sample_vectors(self, index, sample_vectors,
            factor_function):

        noise = 0#.003
        sample_vectors_without_index = np.copy(sample_vectors)
        sample_vectors_without_index[..., index] = np.zeros(sample_vectors.shape[0])

        unique_sample_vectors, frequency_counts = np.unique(sample_vectors_without_index, axis=0, return_counts=True)

        max_value_for_0 = np.max(np.apply_along_axis(factor_function, 1, unique_sample_vectors)*frequency_counts)

        unique_sample_vectors[..., index] = np.ones(unique_sample_vectors.shape[0])
        max_value_for_1 = np.max(np.apply_along_axis(factor_function, 1, unique_sample_vectors)*frequency_counts)

        new_message = self.__normalize(np.array([max_value_for_0, max_value_for_1]) + noise)

        return new_message

    def __apply_factor_function(self, index, sample_vector, factor_function):
        new_vector = np.copy(sample_vector)
        new_vector.put(index, 0)
        entry0 = factor_function(new_vector)
        new_vector.put(index, 1)
        entry1 = factor_function(new_vector)
        return np.array([entry0, entry1])


    def __normalize(self, message):
        noise = 1#np.array([0,1])*np.exp(np.random.normal())
        return message/float(message.sum()) if message.sum() > 0 else np.array([0.5, 0.5])*noise

