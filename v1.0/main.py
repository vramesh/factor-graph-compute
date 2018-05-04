from redis import Redis
from factor_graph import FactorGraph
import time

r = Redis()
r.flushall()


config = {
    "algorithm": "sum_product",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous"
}
path_to_input_file = "examples/hmm_simple_factor_graph_ver_7_new_ui.txt"

fg = FactorGraph(path_to_input_file, config)
fg.run()
time.sleep(10)
fg.print_solution()