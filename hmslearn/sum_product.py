import numpy as np
#from collections import namedtuple
#from sklearn.utils.extmath import cartesian
#from scipy.stats import mode
#from scipy.stats import itemfreq 
from attrdict import AttrDict
from collections import OrderedDict
from functools import reduce
import pdb
#from hmm_factor_functions import y1_observation, y2_observation#, transition_factor_function


def sum_product_update_var(state, messages, sender_id, recipient_id,
        from_node_id):
    if recipient_id == from_node_id:
        return
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    message_product = np.array(state)
    for _, message in messages.items():
        if message is not None:
            message_product *= np.array(message)
    if messages[recipient_id] is not None:
        outgoing_message = normalize_message(message_product/np.array(messages[recipient_id]))
    else:
        outgoing_message = normalize_message(message_product)
    return outgoing_message

def sum_product_update_fac(state, messages, sender_id, recipient_id,
        from_node_id):
    if recipient_id == from_node_id:
        return 

    state_numpy = np.array(state)
    dimension = len(state_numpy.shape)
    if dimension == 2:
        outgoing_message = np.dot(np.array(state),np.array(messages[from_node_id])) # not always correct

    elif dimension == 3:
        if recipient_id > from_node_id:
            outgoing_message = np.dot(np.array(state[0]),np.array(messages[from_node_id]))
        else:
            outgoing_message = np.dot(np.array(state[1]),np.array(messages[from_node_id]))


    # variable_index = sender_id[1:]
    # factor_index = recipient_id[1:]
    # factor_function = transition_factor_function 

    # messages = OrderedDict(sorted(messages.items(), key=lambda t: t[0]))
    # node_from_node_index = {index: node_id_message[0] for index, node_id_message in
    #         enumerate(messages.items())}

    # node_index_from_node_id = {node_id_message[0]: node_index for node_index,
    #         node_id_message in enumerate(messages.items())}
            
    # recipient_index = node_index_from_node_id[recipient_id] 

    # outgoing_message = np.dot(np.array(state[recipient_index]),np.array(messages[from_node_id]))

    # index_from_value = {-1: 0, 1: 1}

    # factor_function_inputs = cartesian(np.array([np.array([-1,1])]*(len(messages))))
    # factor_function_inputs[factor_function_inputs[:,recipient_index].argsort()]

    # outgoing_message = np.array([])
    # for input_vector in factor_function_inputs:
    #     factor_function_value = factor_function(input_vector)

    #     for node_index, message_value in enumerate(input_vector):
    #         node_id = node_from_node_index[node_index]
    #         if node_id != recipient_id:
    #             node_message = messages[node_id]
    #             message_to_multiply = node_message[index_from_value[message_value]] 
    #             factor_function_value *= message_to_multiply
    #     outgoing_message = np.append(outgoing_message, factor_function_value)

    # outgoing_message = outgoing_message.reshape((2, int(outgoing_message.shape[0]/2))) 
    # outgoing_message = np.sum(outgoing_message, axis=1)

    return outgoing_message

def normalize_message(message):
    return message/message.sum() if message.sum() > 0 else np.array([0.5, 0.5])

