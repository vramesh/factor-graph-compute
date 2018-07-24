def page_rank_update_var(state, messages, sender_id, recipient_id, from_node_id = None):
    print("var", state, sender_id, recipient_id, messages)
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    # print(state,variable_index,factor_index)
    if state==0:
        return 0
    else:
        if variable_index == factor_index: # m_{vi->fi} = 0
            return 0
        else:
            return messages["f"+variable_index]/state # m_{vj->fi} = m_{fj->vj}/x_{vj}

def page_rank_update_fac(state, messages, sender_id, recipient_id, from_node_id = None, alpha=0.1):
    print("fac", state, sender_id, recipient_id, messages)
    variable_index = recipient_id[1:]
    factor_index = sender_id[1:]
    if variable_index != factor_index: # m{fi->vj} =0 
        return 0
    else:
        return sum(list(messages.values())) - messages["v"+factor_index] # for now, assume that alpha=1, so we dont need to use n
