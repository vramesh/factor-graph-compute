from redis import Redis
from factor_graph import FactorGraph
import time
import subprocess

r = Redis()
subprocess.Popen("redis-server")
r.flushall()


config = {
    "algorithm": "sum_product",
    "pubsub_choice": "redis",
    "synchronous": "asynchronous",
    "number_of_iter": 100
}
path_to_input_file = "examples/hmm_simple_factor_graph_ver_7_new_ui.txt"

fg = FactorGraph(path_to_input_file, config)
fg.run()
time.sleep(10)
fg.print_solution()