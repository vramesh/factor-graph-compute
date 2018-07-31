# Hermes

Hermes is a framework for machine and reinforcement learning that is optimized for distributed systems and speed. The framework is based on the factor graph data structure used in statistical inference.

## Installation

To install Hermes, simply:
```
pip install hmslearn
```

## Tutorial 

This tutorial performs belief propagation/sum-product message passing on the following graph. Nodes v01, v02, and v03 are either 0 or 1, determined randomly. Nodes v1, v2, and v3 contain values that encompass the probability that v01, v02, and v03 are either 0 or 1. Better explanation of the graph goes here.

![](https://raw.githubusercontent.com/vramesh/factor-graph-compute/development/hmm_sum_product2.png)

### Getting Started

We start by importing all the necessary packages.


```python
from hmslearn import FactorGraph
import numpy as np
```

Define all of the update functions for variable and factor nodes. Make a list containing all update functions.

```python
def normalize_message(message):
    return message/message.sum() if message.sum() > 0 else np.array([0.5, 0.5])


def sum_product_update_var(state, messages, sender_id, recipient_id,
        from_node_id):
    if recipient_id == from_node_id:
        return
    variable_index = sender_id[1:]
    factor_index = recipient_id[1:]
    message_product = np.array(state)
    for _, message in messages.items():
        if message is not None:
            message_product *= np.array(message)
    if messages[recipient_id] is not None:
        outgoing_message = normalize_message(message_product/np.array(messages[recipient_id]))
    else:
        outgoing_message = normalize_message(message_product)
    return outgoing_message



def sum_product_update_fac(state, messages, sender_id, recipient_id,
        from_node_id):
    if recipient_id == from_node_id:
        return 

    state_numpy = np.array(state)
    dimension = len(state_numpy.shape)
    if dimension == 2:
        outgoing_message = np.dot(np.array(state),np.array(messages[from_node_id])) # not always correct

    elif dimension == 3:
        if recipient_id > from_node_id:
            outgoing_message = np.dot(np.array(state[0]),np.array(messages[from_node_id]))
        else:
            outgoing_message = np.dot(np.array(state[1]),np.array(messages[from_node_id]))

    return outgoing_message


function_list = [variable_node_update_function, factor_node_update_function]
```

Now make a new file called "graph.txt" and save it in the same directory. This file specifies the structure of the factor graph in the format below. The factor graph shown above translates to the file below.

```
Edges
v01 f11 [0.0,0.0,1.0]
v02 f22 [1.0,0.0,0.0]
v03 f33 [1.0,0.0,0.0]
f11 v1 None
v1 f12 None
f12 v1 None
v2 f12 None
f12 v2 None
f22 v2 None
f33 v3 None
v2 f23 None
v3 f23 None
f23 v2 None
f23 v3 None
Vertices
v01 None sum_product_update_var
v02 None sum_product_update_var
v03 None sum_product_update_var
v1 [0.75,0.25] sum_product_update_var
v2 [1.0,1.0] sum_product_update_var
v3 [1.0,1.0] sum_product_update_var
f11 [[0.9,0.05,0.05],[0.05,0.05,0.9]] sum_product_update_fac
f22 [[0.9,0.05,0.05],[0.05,0.05,0.9]] sum_product_update_fac
f33 [[0.9,0.05,0.05],[0.05,0.05,0.9]] sum_product_update_fac
f12 [[[0.75,0.25],[0.25,0.75]],[[0.75,0.25],[0.25,0.75]]] sum_product_update_fac
f23 [[[0.75,0.25],[0.25,0.75]],[[0.75,0.25],[0.25,0.75]]] sum_product_update_fac
```
Last, we define a config file, make a factor graph object, run it, and acquire our results. 

```python
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
2. Write benchmarks and unit tests for sum and max product.
3. Expand to CUDA.
4. Extend algorithms to gradient descent, classical machine learning, etc.
