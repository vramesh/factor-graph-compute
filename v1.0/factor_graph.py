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
        self.factor_nodes = list() #list of Node objects
        self.variable_nodes = list() #list of Node objects
        self.edges = list() #list of Edge objects
        self.config = config
        self.algorithm = config["algorithm"]
        self.path_to_input_file = path_to_input_file

        #self.broker = Broker()
        self.read_file()

    def read_file(): # may need to design the format of input file for each algorithm
        if self.algorithm == "page_rank": # assume the index is 1,2,...,n
            all_node_index = set()
            with open(self.path_to_input_file, "r") as f:
                all_lines = f.readlines()
                for line in all_lines:
                    line_split = line.split()
                    if len(line_split) == 2:
                        x = int(line_split[0])
                        y = int(line_split[1])
                        all_node_index.add(x)
                        all_node_index.add(y)
                        #Edge.
            node_num = max(all_node_index)
            for i in range(node_num):
                initial_messages_to_var = dict([(j,0) if j!=i else (j,1/node_num) for j in range(node_num)])
                initial_messages_to_fac = dict([(j,0) for j in range(node_num)])
                variable_node_state = NodeState(ALGORITHM_TO_UPDATE_FUNCTIONS[self.algorithm]["update_var"],
                                           initial_messages_to_var,
                                           i,
                                           "variable", # node_type
                                           list(range(node_num)), # neighbour
                                           StateStore())
                variable_node = Node(i,"variable",None,variable_node_state,self.broker)
                factor_node_state = NodeState(ALGORITHM_TO_UPDATE_FUNCTIONS[self.algorithm]["update_fac"],
                                           initial_messages_to_fac,
                                           i,
                                           "factor", # node_type
                                           list(range(node_num)), # neighbour
                                           StateStore())
                factory_node = Node(i,"factory",None,factory_node_state,self.broker)
                self.variable_nodes.append(variable_node)
                self.factor_nodes.append(factor_node)
        else:
            print("Haven't implement for algorithm " + algorithm)


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
