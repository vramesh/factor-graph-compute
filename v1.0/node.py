from state import NodeStateStore
import numpy as np
import time
import pdb

class Node:
    def __init__(self,node_id,node_type,node_function,initial_node_message_cache,node_data,pubsub):
        self.node_id = node_id
        self.node_type = node_type
        self.node_data = node_data
        self.initial_node_message_cache = initial_node_message_cache

        self.pubsub = pubsub
        self.state_store = NodeStateStore("redis")
        self.state_store.create_node_state(node_id,initial_node_message_cache,node_type,node_data)
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id,node_function)

    def get_initial_message_from_sender(self,sender):
        return self.initial_node_message_cache[sender]

    def get_sender_list(self):
        return self.initial_node_message_cache.keys()

    def receive_messages_from_neighbors(self):
        time.sleep(0.1)
        for sender in self.initial_node_message_cache:
            channel_id = (sender + "_" + self.node_id).encode('ascii') #encode
            self.pubsub.broker.publish(channel_id, self.initial_node_message_cache[sender])

        #for the sake of initializing pubsub running

    def get_current_cached(self):
        return NodeStateStore("redis").fetch_node(self.node_id,"messages")
    def get_final_state(self, algorithm):
        node_cache = self.state_store.fetch_node(self.node_id, 'messages')
        if algorithm == 'max_product' or algorithm == 'sum_product':
            unnormalized_probability_vector = np.prod(np.array([message for _, message in
                node_cache.items()]))
            normalized_probability_vector = \
            unnormalized_probability_vector/unnormalized_probability_vector.sum()
            return np.argmax(normalized_probability_vector) 
        else:
            return node_cache
