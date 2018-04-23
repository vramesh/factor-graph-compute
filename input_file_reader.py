from node import Node
from edge import Edge
from factor_graph import FactorGraph

class FactorGraphReader:
    def register_pubsub_from_pagerank_adjacency_list(path_to_input_file, pubsub, wrapper_var_function, wrapper_fac_function, factor_graph):
        (adjacency_dict_var,adjacency_dict_fac) = FactorGraphReader.read_file_factor_graph(path_to_input_file) #{1:[2,3]}
        num_node = len(adjacency_dict_var)

        for variable_id in adjacency_dict_var:
            initial_messages_var = dict(adjacency_dict_var[variable_id])
            node_data = len(adjacency_dict_var[variable_id])-1
            variable_node = Node(variable_id,"variable",wrapper_var_function,initial_messages_var,node_data,pubsub)
            factor_graph.variable_nodes.append(variable_node)

        for factor_id in adjacency_dict_fac:
            initial_messages_fac = dict(adjacency_dict_fac[factor_id])
            node_data = 0
            factor_node = Node(factor_id,"factor",wrapper_fac_function,initial_messages_fac,node_data,pubsub)
            factor_graph.factor_nodes.append(factor_node)

        for variable_id in adjacency_dict_var:
            for (factor_id,initial_message) in adjacency_dict_var[variable_id]:
                channel_name = variable_id + "_" + factor_id
                edge = Edge(variable_id,factor_id, channel_name, pubsub)
                factor_graph.edges.append(edge)

        for factor_id in adjacency_dict_fac:
            for (variable_id,initial_message) in adjacency_dict_fac[factor_id]:
                channel_name = factor_id + "_" + variable_id
                edge = Edge(factor_id,variable_id, channel_name, pubsub)
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



class InputFileReader:
	def __init__(self, pubsub):
		self.pubsub = pubsub
		self.factor_graph = Factor_Graph()

	def read_input_file(self, path_to_input_file, algorithm):

		update_var_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[algorithm]["update_var"]
        wrapper_var_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_var_function, self.pubsub)
        update_fac_function  = ALGORITHM_TO_UPDATE_FUNCTIONS[algorithm]["update_fac"]
        wrapper_fac_function = lambda incoming_message: RedisCallbackClass.message_pass_wrapper_for_redis(incoming_message, update_fac_function, self.pubsub)


		factor_graph_file = open(path_to_input_file)
		for line in factor_graph_file:
			elements = line.split(";") #id, isvariable, inital_message, separated by ; 
			node_id =  elements[0]
			is_variable = True if elements[1] == 0 else False
			initial_messages = elements[2]
			node_data = elements[3]

			if is_variable:
				node = Node(node_id,"variable",wrapper_var_function,initial_messages,node_data,self.pubsub)
				self.factor_graph.variable_nodes.append(node)
			else:
				node = Node(node_id,"factor",wrapper_fac_function,initial_messages,node_data,self.pubsub)
				self.factor_graph.factor_nodes.append(node)

		return self.factor_graph

