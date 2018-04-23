from node import Node
from edge import Edge
from redis_callback_class import RedisCallbackClass
from node_update_functions import ALGORITHM_TO_UPDATE_FUNCTIONS

class FactorGraphReader:
    def make_factor_graph(factor_graph):
        if factor_graph.algorithm == "page_rank":
            return FactorGraphReader.register_pubsub_from_pagerank_adjacency_list(factor_graph)


    def register_pubsub_from_pagerank_adjacency_list(factor_graph):
        (adjacency_dict_var,adjacency_dict_fac) = FactorGraphReader.read_file_factor_graph(factor_graph.path_to_input_file) #{1:[2,3]}
        num_node = len(adjacency_dict_var)
        update_var_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[factor_graph.algorithm]["update_var"]
        update_fac_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[factor_graph.algorithm]["update_fac"]
        wrapper_var_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_var_function, factor_graph.pubsub)
        wrapper_fac_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_fac_function, factor_graph.pubsub)

        for variable_id in adjacency_dict_var:
            initial_messages_var = dict(adjacency_dict_var[variable_id])
            node_data = len(adjacency_dict_var[variable_id])-1
            variable_node = Node(variable_id,"variable",wrapper_var_function,initial_messages_var,node_data,factor_graph.pubsub)
            factor_graph.variable_nodes.append(variable_node)

        for factor_id in adjacency_dict_fac:
            initial_messages_fac = dict(adjacency_dict_fac[factor_id])
            node_data = 0
            factor_node = Node(factor_id,"factor",wrapper_fac_function,initial_messages_fac,node_data,factor_graph.pubsub)
            factor_graph.factor_nodes.append(factor_node)

        for variable_id in adjacency_dict_var:
            for (factor_id,initial_message) in adjacency_dict_var[variable_id]:
                channel_name = variable_id + "_" + factor_id
                edge = Edge(variable_id,factor_id, channel_name, factor_graph.pubsub)
                factor_graph.edges.append(edge)

        for factor_id in adjacency_dict_fac:
            for (variable_id,initial_message) in adjacency_dict_fac[factor_id]:
                channel_name = factor_id + "_" + variable_id
                edge = Edge(factor_id,variable_id, channel_name, factor_graph.pubsub)
                factor_graph.edges.append(edge)

        return factor_graph

    def read_file_factor_graph(path_to_input_file): 
        adjacency_dict_var = dict() #key: variable index, value: list of factor index
        adjacency_dict_fac = dict()
        with open(path_to_input_file) as f:
            all_lines = f.readlines()
            for line in all_lines:
                [x,y,initial_incoming_message] = line.split()
                initial_incoming_message = float(initial_incoming_message)

                if y[0]=="v":
                    add_to_adjacency_dict = adjacency_dict_var
                elif y[0]=="f":
                    add_to_adjacency_dict = adjacency_dict_fac

                if y in add_to_adjacency_dict:
                    add_to_adjacency_dict[y].append((x,initial_incoming_message))
                else:
                    add_to_adjacency_dict[y] = [(x,initial_incoming_message)]

        return (adjacency_dict_var,adjacency_dict_fac)