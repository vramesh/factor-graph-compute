import inspect
import pagerank_converter

all_functions = inspect.getmembers(pagerank_converter, inspect.isfunction)
print(all_functions)
print(all_functions[0][0] == "convert_adjacency_list_input_file_to_pagerank_factor_graph_and_register_with_pubsub")

