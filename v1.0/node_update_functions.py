from max_product import max_product_update_var, max_product_update_fac
decrypt = lambda x: float(x.decode("ascii")) if type(x) == bytes else x 

def print_bye(a=None, b=None, c=None, d=None):
    return "bye"

def print_hi(a=None, b=None, c=None, d=None):
    return "hi"

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": lambda state, messages, sender_id, recipient_id: 0 if state==0 else (messages["f"+sender_id[1:]]/state if sender_id[1:]!=recipient_id[1:] else 0) ,
        "update_fac": lambda state, messages, sender_id, recipient_id: sum(list(messages.values())) - messages["v"+sender_id[1:]] if sender_id[1:] == recipient_id[1:] else 0
    },

    "page_rank_fake": {
        "update_var": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+1,
        "update_fac": lambda state, messages, sender_id, recipient_id: messages[recipient_id]+1
    },

    "max_product": {
        "update_var": max_product_update_var,
        "update_fac": max_product_update_fac
    }
}
