decrypt = lambda x: float(x.decode("ascii")) if type(x) == bytes else x 

def print_bye(a=None, b=None, c=None, d=None):
    print("bye")

def print_hi(a=None, b=None, c=None, d=None):
    print("hi")

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
        "update_var": print_hi,
        "update_fac": print_bye
    }
}
