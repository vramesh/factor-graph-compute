from multiprocessing import Manager
from redis import StrictRedis, Redis
import pickle as pickle

class NodeStateStore: #node state manager
    def __init__(self, state_store_spec):
        if state_store_spec == "dict":
            self.state_store_spec = DictNodeStateStore()
        elif state_store_spec == "redis":
            self.state_store_spec = RedisNodeStateStore()

    def update_node(self, incoming_message, node_id):
        return self.state_store_spec.update_node_messages(incoming_message, node_id)

    def fetch_node(self, node_id):
        self.state_store_spec.fetch_node(node_id)

    def create_node_state(self, node_id, initial_messages, node_type, node_data):
        self.state_store_spec.create_node_state(node_id, initial_messages, node_type, node_data)


class RedisNodeStateStore:
    def __init__(self):
        pass

    def update_node_messages(self, incoming_message, node_id):
        redis = Redis()
        #update here

        redis.hset(node_id, "messages", updated_message)
        return redis.hget(node_id, "messages")

    def fetch_node_messages(self, node_id):
        redis = Redis()
        return pickle.loads(redis.hget(node_id, "messages"))

    def create_node_state(self, node_id, initial_messages, node_type, node_data):
        #id -> {"messages": , "type", "data"}
        redis = Redis()
        redis.hmset(node_id, {"messages": initial_messages, "node_type": node_type,
            "node_data": node_data})
        return True








#not used
class DictNodeStateStore:
    def __init__(self):
        self.manager = Manager()

        self.node_state_database = self.manager.dict() #node_id to node_state_object

    def update_node(self, incoming_message, node_id):
        self.node_state_database[node_id] = incoming_message
        return True

    def fetch_node(self, node_id):
        return self.node_state_database[node_id]