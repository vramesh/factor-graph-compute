from state import NodeStateStore
from redis_callback_class import RedisCallbackClass
import numpy as np
import time

class Node:
    def __init__(self,node_id,node_type,node_function,initial_node_message_cache,
                    node_data,pubsub,outgoing_neighbors, number_of_iter):
        self.node_id = node_id
        self.node_type = node_type
        self.node_data = node_data
        self.outgoing_neighbors_with_values = outgoing_neighbors
        self.outgoing_neighbors_list = list(outgoing_neighbors.keys())
        self.initial_node_message_cache = initial_node_message_cache

        self.pubsub = pubsub
        self.state_store = NodeStateStore("redis")
        self.state_store.create_node_state(node_id,initial_node_message_cache,node_type,node_data,self.outgoing_neighbors_list, number_of_iter)
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id,node_function)

    def get_initial_message_from_sender(self,sender):
        return self.initial_node_message_cache[sender]

    def get_sender_list(self):
        return self.initial_node_message_cache.keys()

    def send_initial_messages(self):
        # time.sleep(0.1)  # veru crucial, don't know why
        for neighbor in self.outgoing_neighbors_with_values:
            channel_id = (self.node_id + "_" + neighbor).encode('ascii') #encode
            print("publish from " + self.node_id + " to " + neighbor)
            new_outgoing_message = self.outgoing_neighbors_with_values[neighbor]
            RedisCallbackClass.propagate_message(channel_id, new_outgoing_message, self.pubsub)

    def get_current_cached(self):
        return NodeStateStore("redis").fetch_node(self.node_id,"messages")

    def get_final_state(self, algorithm):
        node_cache = self.state_store.fetch_node(self.node_id, 'messages')
        if algorithm == 'max_product' or algorithm == 'sum_product':
            print(node_cache)
            if len(node_cache.items()) > 1:
                un_normalized_probability_vector = np.prod(np.array([message for _, message in
                    node_cache.items()]), axis=0)
            else:
                un_normalized_probability_vector = np.array([message for _,
                    message in node_cache.items()])[0]
            normalized_probability_vector = \
            un_normalized_probability_vector/un_normalized_probability_vector.sum()
            return normalized_probability_vector
#            return np.argmax(normalized_probability_vector) 
        else:
            return node_cache
