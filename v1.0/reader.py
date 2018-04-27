from node import Node
from edge import Edge
import ast

class FactorGraphReader:
    def register_pubsub_from_factor_graph_file(path_to_input_file, pubsub, wrapper_var_function, wrapper_fac_function, factor_graph):
        (adjacency_dict_var,adjacency_dict_fac, outgoing_neighbors_dict, node_dict_var, node_dict_fac) =\
         FactorGraphReader.read_file_factor_graph(path_to_input_file) #{1:[2,3]}
        num_node = len(adjacency_dict_var)

        for variable_id in adjacency_dict_var:
            initial_messages_var = dict(adjacency_dict_var[variable_id])
            node_data = node_dict_var[variable_id]
            outgoing_neighbors = outgoing_neighbors_dict[variable_id]
            variable_node = Node(variable_id,"variable",wrapper_var_function,initial_messages_var,node_data,pubsub,outgoing_neighbors)
            factor_graph.variable_nodes.append(variable_node)

        for factor_id in adjacency_dict_fac:
            initial_messages_fac = dict(adjacency_dict_fac[factor_id])
            node_data = node_dict_fac[factor_id]
            outgoing_neighbors = outgoing_neighbors_dict[factor_id]
            factor_node = Node(factor_id,"factor",wrapper_fac_function,initial_messages_fac,node_data,pubsub,outgoing_neighbors)
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
        outgoing_neighbors_dict = dict()
        node_dict_var = dict()
        node_dict_fac = dict()
        with open(path_to_input_file) as f:
            all_lines = f.readlines()
            num_lines = len(all_lines)
            if num_lines == 0:
                raise ValueError("The input factor graph file is empty")
            if all_lines[0].split() != ["Edges"]:
                raise ValueError("In input factor graph, first line must be 'Edges'")
            if num_lines == 1:
                raise ValueError("The input factor graph file does not have any edges")
            line_index = 1
            has_vertices = False

            while line_index < num_lines:
                line = all_lines[line_index]
                if line.split() == ["Vertices"]:
                    has_vertices = True
                    break
                [x,y,initial_incoming_message] = line.split()
                # initial_incoming_message = float(initial_incoming_message)
                if initial_incoming_message == "None":
                    initial_incoming_message = None
                else:
                    initial_incoming_message = ast.literal_eval(initial_incoming_message)  # may be changed to pickle
                
                if y[0] == "v":
                    add_to_adjacency_dict = adjacency_dict_var
                elif y[0] == "f":
                    add_to_adjacency_dict = adjacency_dict_fac
                else:
                    raise ValueError("Name format is wrong")

                if x not in outgoing_neighbors_dict:
                    outgoing_neighbors_dict[x] = {y:initial_incoming_message}
                else:
                    outgoing_neighbors_dict[x][y] = initial_incoming_message

                if y in add_to_adjacency_dict:
                    add_to_adjacency_dict[y].append((x,initial_incoming_message))
                else:
                    add_to_adjacency_dict[y] = [(x,initial_incoming_message)]

                line_index += 1

            if not has_vertices:
                raise ValueError("In input factor graph, first line must be 'Vertices'")

            while line_index < num_lines:
                line = all_lines[line_index]
                if len(line.split()) == 2:
                    [node,state] = line.split()
                    state = ast.literal_eval(state)  # may be changed to pickle
                    if node[0] == "v":
                        node_dict_var[node] = state
                    elif node[0] == "f":
                        node_dict_fac[node] = state
                line_index += 1


        return (adjacency_dict_var,adjacency_dict_fac, outgoing_neighbors_dict, node_dict_var, node_dict_fac)














