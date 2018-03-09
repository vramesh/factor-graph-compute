import numpy as np
from collections import namedtuple
from sklearn.utils.extmath import cartesian
from scipy.stats import mode
from scipy.stats import itemfreq 


class MaxProductVariableNode():
    def update_edges(edges):
        node_state = __node_state_from_edges(edges)
        new_edges = __edges_from_node_state(node_state, edges)
        return new_edges

    def update_edge_marginals(edges):
        marginal = __marginals_from_edges(edges)
        edges_with_marginals = __edges_from_marginals(marginal, edges)
        return edges_with_marginals 

    def __node_state_from_edges(edges):
#        if any([edge.decimation_status for edge in edges]) == 1:
#            message_product = np.array([0,1])
#        else:
        variable_cost_mean = edges[0].variable_cost
        variable_cost = variable_cost_mean#np.sign(variable_cost_mean)*np.random.exponential(np.abs(variable_cost_mean))
        message_product = np.array([1, np.exp(-1*variable_cost)])*__compute_message_product(edges)
#            message_product = self.__compute_message_product(edges)
        return __normalize_message(message_product)

    def __edges_from_node_state(node_state, edges):
        return [__compute_new_neighbor_message(node_state, edge) for edge in edges]

    def __marginals_from_edges(edges):
        unnormalized_marginal = __node_state_from_edges(edges)
        marginal = __normalize_message(unnormalized_marginal)
        return marginal 

    def __edges_from_marginals(marginal, edges):
        [setattr(edge, 'message', marginal) for edge in edges]
        return edges

    # Helper Methods
    def __compute_message_product(edges):
        edge_array = np.array([edge.message for edge in edges])
        message_product = np.prod(edge_array, axis=0) 

        '''
        if message_product[0] == 0 and message_product[1] == 0:
            print "noise case"
            noise = 0.003
#            message_product = np.array([1-noise, 0+noise])
            edge_array_with_noise  = edge_array + noise
            message_product = np.prod(edge_array_with_noise, axis=0) 
        '''
        return message_product

    def __compute_new_neighbor_message(message_product, edge):
    
        new_edge_message = \
        __normalize_message(np.nan_to_num(message_product/edge.message))

        edge.message = new_edge_message
        return edge

    def __normalize_message(message):
        noise = 1#np.array([0,1])*np.exp(np.random.normal())
        return message/float(message.sum()) if message.sum() > 0 else np.array([0.5, 0.5])*noise


def update_fac_mp(messages):
    pass

def update_var_mp(state, messages, sender_id, receipient_id):
    print("hello")
    # massage into numpy array
    #print(incoming_messages)

   # outgoing_messages = MaxProductVariableNode.update_edges(incoming_messages)
   # print("should never get here", outgoing_messages)
    # massage into right output
   # return outgoing_messages





