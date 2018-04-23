from redis import Redis
from factor_graph import FactorGraph

def main():
	r = Redis()
	r.flushall()
	#need to create connection here

	config = {
	    "algorithm": "page_rank",
	    "pubsub_choice": "redis",
	    "synchronous": "asynchronous"
	}

	path_to_input_file = "examples/pagerank_factor_graph_example_adjadjacency_list.txt"
	try_fg = FactorGraph(path_to_input_file, config)
	try_fg.run()