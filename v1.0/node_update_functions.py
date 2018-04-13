# from max_product import update_var_mp

decrypt = lambda x: float(x.decode("ascii")) if type(x) == bytes else x 

def print_bye(a=None, b=None, c=None, d=None):
    print("bye")

def print_hi(a=None, b=None, c=None, d=None):
    print("hi")

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": lambda state, messages, sender_id, recipient_id: 0 if state==0 else (messages["f"+sender_id[1:]]/state if sender_id[1:]!=recipient_id[1:] else 0) ,
        "update_fac": lambda state, messages, sender_id, recipient_id: sum(list(messages.values())) - messages["v"+sender_id[1:]] if sender_id[1:] == recipient_id[1:] else 0
    },

    "page_rank_fake": {
        "update_var": lambda state, messages, sender_id, recipient_id: decrypt(messages[recipient_id])+1,
        "update_fac": lambda state, messages, sender_id, recipient_id: decrypt(messages[recipient_id])+1
    },

    "max_product": {
        "update_var": print_hi,#lambda state, messages, sender_id, recipient_id: update_var_mp(state, messages, sender_id, receipient_id),
        "update_fac": print_bye
    }
}


def page_rank_update_var(state, messages, sender_id, recipient_id):
    if state==0:
        return 0
    else:
        if sender_id[1:] != recipient_id[1:]:
            return 0
        else:
            return decrypt(messages["f"+sender_id[1:]]) # Need to be change _> careful about decrypt

def page_rank_update_fac(state, messages, sender_id, recipient_id):
    if sender_id[1:] != recipient_id[1:]:
        return 0
    else:
        return sum(list(messages.values())) - messages["v"+sender_id[1:]]  # Need to be change _> careful about decrypt

def page_rank_fake_update_var(state, messages, sender_id, recipient_id):
    pass

def page_rank_fake_update_fac(state, messages, sender_id, recipient_id):
    pass

