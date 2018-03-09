from state import StateStore, NodeState
from Pubsub import Publisher, Subscriber, Channel, PubSub, Broker

ALGORITHM_TO_UPDATE_FUNCTIONS = \
{
    "page_rank": {
        "update_var": lambda state, messages, sender_index, recipient_index: messages[sender_index]/state if sender_index!=recipient_index else 0 ,
        "update_fac": lambda state, messages, sender_index, recipient_index: sum([messages.values()]) - messages[sender_index] if sender_index == recipient_index else 0
    }
}

class FactorGraph:
    def __init__(self, path_to_input_file, config):
        #important
        self.factor_nodes = list() 
        self.variable_nodes = list() 
        self.edges = list() 
        self.pubsub = Pubsub(config['pubsub_choice'])

        #less important ones
        self.config = config
        self.algorithm = config["algorithm"]
        self.path_to_input_file = path_to_input_file

        #register and initialize pubsub processes
        self.initialize_nodes_and_edges() #populates nodes and edges
        self.pubsub.start()

    def initialize_nodes_and_edges(): 
        pass
            


class FactorGraphService:
    def __init__(self):
        pass

    def create(self, path_to_input_file, config):
        factor_graph = FactorGraph(path_to_input_file, config)
        return factor_graph

    def run(self, factor_graph):
        answer_dictionary = dict()
        return answer_dictionary


class Edge:
    def __init__(self, edge_name):
        self.channel = Channel(edge_name)
        self.channel.register(self.pubsub)
        # Pubsub.registerChannel(chan_id)


class Node:
    def __init__(self, node_id, new_type, node_function, node_state, broker):
        self.node_id = node_id
        self.node_type = node_type
        self.node_state = node_state
        self.broker = broker
        #may not need node_dunction

        # Connect to PubSub
        # Pubsub.registerPublisher(publisher_id)
        # Pubsub.registerSub(sub_id)
        # Pubsub.subscribt(sub_id, cha_id)

        self.publisher = Publisher(node_id)
        self.subscriber = Subscriber(node_id, self.broker)
        self.publisher.register()
        self.subscriber.register(self.broker)


def message_pass(self, incoming_message, all_channels): 
    #main callback for pubsub
    #pubsubs handles active listening
    updated_state = self.__update_state(incoming_message)
    for channel_name in all_channels:
        new_outgoing_message = self.__compute_outgoing_message(updated_state, channel_name)
        self.__propagate_message(new_outgoing_message, channel_name)

def __update_state(self, incoming_message):
    new_full_state = self.node_state.update(incoming_message, self.node_id)
    return new_full_state

def __compute_outgoing_message(self, updated_state, channel_name):
    new_outgoing_message = ""  # need callback function here, which in turn need permanent state, all current messages, so node_state need to send it here?
    return new_outgoing_message

def __propagate_message(self, new_outgoing_message):
    self.publisher.publish(new_outgoing_message)

# It's a mess here. Publisher, Subscriber is in Node, but all the channel information
# is in node_state. It is unclear if callback_function should be in both or not, and it seem
# like we have to send lots of unnecessary data between node and node_state
