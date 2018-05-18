def convert_to_page_rank_factor_graph_file(path_to_input_file,path_to_output_file):
    with open(path_to_input_file, "r") as f:
        all_lines = f.readlines()
        num_node = int(all_lines[0])
        all_edges = list()
        for line in all_lines[1:]:
            [x,y] = line.split()
            all_edges.append((x,y))

    with open(path_to_output_file, "w") as f:
        for node_index in range(num_node):
            variable_node_name = "v"+str(node_index)
            factor_node_name = "f"+str(node_index)
            edge_description = "{0} {1} {2}\n".format(variable_node_name,factor_node_name,0)
            f.write(edge_description)
            edge_description = "{0} {1} {2:.3f}\n".format(factor_node_name,variable_node_name,1/num_node)
            f.write(edge_description)
        for x,y in all_edges:
            variable_node_name = "v"+x
            factor_node_name = "f"+y
            edge_description = "{0} {1} {2}\n".format(variable_node_name,factor_node_name,0)
            f.write(edge_description)
            edge_description = "{0} {1} {2}\n".format(factor_node_name,variable_node_name,0)
            f.write(edge_description)


# convert_to_page_rank_factor_graph_file("examples/pagerank_graph_adjaceny_list_example.txt", \
#                                        "examples/result_page_rank_factor_graph.txt")