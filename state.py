from multiprocessing import Manager
from redis import StrictRedis, Redis
import ast
import pickle

class NodeStateStore: #node state manager
    def __init__(self, state_store_spec):
        if state_store_spec == "redis":
            self.state_store_spec = RedisNodeStateStore()

    def update_node(self, incoming_message, node_id):
        return self.state_store_spec.update_node_messages(incoming_message, node_id)

    def fetch_node(self, node_id, field):
        return self.state_store_spec.get_data(node_id,field)

    def create_node_state(self, node_id, initial_messages, node_type, node_data, outgoing_neighbors, number_of_iter):
        self.state_store_spec.create_node_state(node_id, initial_messages, node_type, node_data, outgoing_neighbors, number_of_iter)

    def countdown_by_one(self, node_id):
        self.state_store_spec.countdown_by_one(node_id)


class RedisNodeStateStore:
    def __init__(self):
        self.redis = Redis()

    def update_node_messages(self, message_to_be_cached, node_id):
        node_id = str(node_id)
        previous_message = self.get_data(node_id, "messages")
        channel_name = message_to_be_cached["channel"]
        from_node = channel_name.split("_")[0]
        new_message = message_to_be_cached["data"]  # careful if it is binary or str
        previous_message[from_node] = new_message
        to_be_set_message = previous_message
        self.set_data(node_id,to_be_set_message,"messages")
        return to_be_set_message

    def countdown_by_one(self, node_id):
        # self.redis.hincrby(node_id, 'stop_countdown', -1)
        current_countdown = self.get_data(node_id,'stop_countdown')
        self.set_data(node_id,current_countdown-1,'stop_countdown')

    def create_node_state(self, node_id, initial_messages, node_type, node_data, outgoing_neighbors,
            stop_countdown):
        #id -> {"messages": , "type", "data"}
        pickle_initial_messages = pickle.dumps(initial_messages)
        pickle_node_type = pickle.dumps(node_type)
        pickle_node_data = pickle.dumps(node_data)
        pickle_outgoing_neighbors = pickle.dumps(outgoing_neighbors)
        pickle_stop_countdown = pickle.dumps(stop_countdown)
        data_dict = {"messages": pickle_initial_messages, "node_type": pickle_node_type,
            "node_data": pickle_node_data, "stop_countdown": pickle_stop_countdown,
            "outgoing_neighbors": pickle_outgoing_neighbors}
        self.redis.hmset(node_id, data_dict)
        return True

    def get_data(self,node_id,field,is_string=False): # pickle back to str or dict 
        # self.lock_dict[node_id].acquire()
        message = self.redis.hget(node_id, field)
        # self.lock_dict[node_id].release()
        unpickle_message = pickle.loads(message)
        return unpickle_message

    def set_data(self, node_id, to_be_set_message, field): # if we want to pickle, pickle here
        pickle_message = pickle.dumps(to_be_set_message)
        # self.lock_dict[node_id].acquire()
        self.redis.hset(node_id, field, pickle_message)
        # self.lock_dict[node_id].release()
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






