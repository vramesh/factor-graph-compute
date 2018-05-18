from state import NodeStateStore

class Edge:
    def __init__(self, from_node_id, to_node_id, edge_id, pubsub):
        self.pubsub = pubsub
        self.pubsub.register_channel(edge_id)
        self.pubsub.register_subscription(to_node_id, edge_id)