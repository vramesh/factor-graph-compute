class StateStore: #node state manager
    def __init__(self):
        self.node_state_database = dict() #node_id to node_state_object


class NodeState:
    def __init__(self, callback_function, data, node_id, state_store):
        self.node_id = node_id
        self.data = data #dictionary, key of node_id of senders to their last message data
        self.callback_function = callback_function
        self.state_store = state_store

    def update(self, incoming_data, sender):
        self.data['sender'] = incoming_data #some update
        return self.data
