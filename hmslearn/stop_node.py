from state import NodeStateStore
from redis_callback_class import RedisCallbackClass
import numpy as np
import time

class StopNode:
    def __init__(self,node_id,pubsub,time_till_stop):
        self.node_id = node_id
        self.time_till_stop = time_till_stop
        self.start_time = time.time()

        node_function = self.reset_timer
        self.pubsub = pubsub
        self.pubsub.register_publisher(node_id)
        self.pubsub.register_subscriber(node_id,node_function)

    def reset_timer(self, incoming_message):
        self.start_time = time.time()

    def get_stop_signal(self):
        while True:
            print("sleeping")
            time.sleep(self.time_till_stop)
            print("done sleeping")
            if time.time() - self.start_time > self.time_till_stop:
                return True
