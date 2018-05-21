from redis import Redis
from factor_graph import FactorGraph
import time

r = Redis()
r.flushall()


config = {
    "algorithm": "sum_product",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous",
    "number_of_iter": 100,
    "time_till_stop": 20
}
path_to_input_file = "examples/hmm_simple_factor_graph_ver_7_new_ui.txt"
output_file = "first_try_output.txt"

fg = FactorGraph(path_to_input_file, config)
fg.run()
fg.get_result(output_file)
