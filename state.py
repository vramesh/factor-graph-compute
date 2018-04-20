from multiprocessing import Manager
from redis import StrictRedis, Redis
import ast

class NodeStateStore: #node state manager
    def __init__(self, state_store_spec):
        if state_store_spec == "redis":
            self.state_store_spec = RedisNodeStateStore()

    def update_node(self, incoming_message, node_id):
        return self.state_store_spec.update_node_messages(incoming_message, node_id)

    def fetch_node(self, node_id, field):
        return self.state_store_spec.get_data(node_id,field)

    def create_node_state(self, node_id, initial_messages, node_type, node_data):
        self.state_store_spec.create_node_state(node_id, initial_messages, node_type, node_data)

    def countdown_by_one(self, node_id):
        self.state_store_spec.countdown_by_one(node_id)


class RedisNodeStateStore:
    def __init__(self):
        self.redis = Redis()

    def update_node_messages(self, message_to_be_cached, node_id):
        node_id = str(node_id)
        previous_message = self.get_data(node_id, "messages")
        channel_name = self.decryptor(message_to_be_cached["channel"],is_string=True)
        from_node = channel_name.split("_")[0]
        new_message = self.decryptor(message_to_be_cached["data"])  # careful if it is binary or str
        previous_message[from_node] = new_message
        to_be_set_message = previous_message
        self.set_data(node_id,to_be_set_message,"messages")
        return to_be_set_message

    def countdown_by_one(self, node_id):
        self.redis.hincrby(node_id, 'stop_countdown', -1)

    def create_node_state(self, node_id, initial_messages, node_type, node_data,
            stop_countdown=10):
        #id -> {"messages": , "type", "data"}
        data_dict = {"messages": initial_messages, "node_type": node_type,
            "node_data": node_data, "stop_countdown": stop_countdown}
        self.redis.hmset(node_id, data_dict)
        return True

    def get_data(self,node_id,field,is_string=False): # pickle back to str or dict 
        message = self.redis.hget(node_id, field)
        return self.decryptor(message)

    def set_data(self, node_id, to_be_set_message, field): # if we want to pickle, pickle here
        self.redis.hset(node_id, field, to_be_set_message)
        return True

    def decryptor(self,data,is_string=False):
        if type(data) == bytes:
            str_data = data.decode("ascii") 
        else:
            str_data = data
        if is_string:
            return_message = str_data
        else:
            return_message = ast.literal_eval(str_data)

        return return_message






