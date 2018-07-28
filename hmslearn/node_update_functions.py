from max_product import max_product_update_var, max_product_update_fac
from sum_product import sum_product_update_var, sum_product_update_fac
from page_rank import page_rank_update_var, page_rank_update_fac

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": page_rank_update_var,
        "update_fac": page_rank_update_fac
    },

    "sum_product": {
        "update_var": sum_product_update_var,
        "update_fac": sum_product_update_fac
    },

    "max_product": {
        "update_var": max_product_update_var,
        "update_fac": max_product_update_fac
    },

    "test": {
        "update_var": lambda state, messages, sender_id, recipient_id, from_node_id: "hi",
        "update_fac": lambda state, messages, sender_id, recipient_id, from_node_id: "bye"
    },

    "page_rank_fake": {
        "update_var": lambda state, messages, sender_id, recipient_id, from_node_id: messages[recipient_id]+1,
        "update_fac": lambda state, messages, sender_id, recipient_id, from_node_id: messages[recipient_id]+1
    },

    "try_pickle": {
        "update_var": lambda state, messages, sender_id, recipient_id, from_node_id: messages[recipient_id]+[1],
        "update_fac": lambda state, messages, sender_id, recipient_id, from_node_id: messages[recipient_id]+[2]
    }
}
