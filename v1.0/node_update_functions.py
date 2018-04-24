from max_product import max_product_update_var, max_product_update_fac
from sum_product import sum_product_update_var, sum_product_update_fac
decrypt = lambda x: float(x.decode("ascii")) if type(x) == bytes else x 

def print_bye(a=None, b=None, c=None, d=None):
    return "bye"

def print_hi(a=None, b=None, c=None, d=None):
    return "hi"

def page_rank_update_var(state, messages, sender_id, recipient_id):
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    # print(state,variable_index,factor_index)
    if state==0:
        return 0
    else:
        if variable_index == factor_index: # m_{vi->fi} = 0
            return 0
        else:
            return messages["f"+variable_index]/state # m_{vj->fi} = m_{fj->vi}/x_{vj}

def page_rank_update_fac(state, messages, sender_id, recipient_id, alpha=0.1):
    variable_index = recipient_id[1:]
    factor_index = sender_id[1:]
    if variable_index != factor_index: # m{fi->vj} =0 
        return 0
    else:
        return sum(list(messages.values())) - messages["v"+factor_index] # for now, assume that alpha=1, so we dont need to use n

def page_rank_fake_update_var(state, messages, sender_id, recipient_id):
    pass

def page_rank_fake_update_fac(state, messages, sender_id, recipient_id):
    pass

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": page_rank_update_var,
        "update_fac": page_rank_update_fac
    },

    "page_rank_fake": {
        "update_var": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+1,
        "update_fac": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+1
    },

    "max_product": {
        "update_var": max_product_update_var,
        "update_fac": max_product_update_fac
    },

    "test": {
        "update_var": print_hi,#lambda state, messages, sender_id, recipient_id: update_var_mp(state, messages, sender_id, receipient_id),
        "update_fac": print_bye
    },

    "try_pickle": {
        "update_var": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+[1],
        "update_fac": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+[2]
    },

    "sum_product": {
        "update_var": sum_product_update_var,
        "update_fac": sum_product_update_fac
    }
}
