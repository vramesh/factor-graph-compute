# Hermes

Hermes is a framework for machine and reinforcement learning that is optimized for distributed systems and speed. The framework is based on the factor graph data structure used in statistical inference.

## Installation

To install Hermes, simply:
```
pip install hmslearn
```

## Getting Started


```
from hmslearn import FactorGraph
```

First, define all of the update functions for variable and factor nodes. Make a list containing all update functions.

```
def variable_node_update_function(state, messages, sender_id, recipient_id,
        from_node_id):
    return "variable node says hi!"



def factor_node_update_function(state, messages, sender_id, recipient_id,
        from_node_id):
    return "factor node says hi!"

function_list = [sum_product_update_fac, sum_product_update_var, normalize_message]
```

Now make a new file called "graph.txt" and save it in the same directory. This file specifies the structure of the factor graph in the format below. In this file, there are two nodes, v1 and f1, each one having an edge pointing at the other node. The factor node f1 has factor_node_update_function as an update function, same goes for variable node v1. 

```
Edges
v1 f1 None
f1 v1 None
Vertices
v1 None variable_node_update_function
f1 None factor_node_update_function
```
Last, we define a config file and make a factor graph object. 

```
config = {
    "algorithm": "sum_product",
    "pubsub_choice": "redis",
    "synchronous": "synchronous",
    "number_of_iter": 100,
    "time_till_stop": 20
}

path_to_input_file = "graph.txt"

fg = FactorGraph(path_to_input_file, config, function_list)
fg.run()

fg.print_solution()
```




## Features Being Actively Developed
1. Get asynchronous mode working.
2. Write benchmarks and unit tests.
3. Expand to CUDA.
4. Extend algorithms to gradient descent, classical machine learning, etc.
