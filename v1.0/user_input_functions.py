import numpy as np
#from collections import namedtuple
#from sklearn.utils.extmath import cartesian
#from scipy.stats import mode
#from scipy.stats import itemfreq 
from attrdict import AttrDict
from collections import OrderedDict
from functools import reduce
import pdb
from hmm_factor_functions import y1_observation, y2_observation#, transition_factor_function


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

    return outgoing_message

def normalize_message(message):
    return message/message.sum() if message.sum() > 0 else np.array([0.5, 0.5])

