# Hermes

Hermes is a framework for machine and reinforcement learning that is optimized for distributed systems and speed. The framework is based on the factor graph data structure used in statistical inference.

## Installation

To install Hermes, simply run:
```shell
pip install hmslearn
```

## Tutorial 

This tutorial performs belief propagation/sum-product message passing for hidden markov models on a simple graph shown below. Nodes v01, v02, and v03 are the observations and can be either 0 or 1, determined randomly. Nodes v1, v2, and v3 contain values that encompass the belief/probability that v01, v02, and v03 are either 0 or 1.

![](https://raw.githubusercontent.com/vramesh/factor-graph-compute/development/hmm_sum_product2.png)

### Getting Started

We start by creating a new file called "graph.txt" that will represent our graph. 

The file should start with the header "Edges", and all new lines following the header should define an edge in this directed graph. The format of each line is as such: source node, destination node, and initial message sent. For instance, the first edge in the file below shows that node v01 sends the message [0.0, 0.0, 1.0] to node f11.

Once all the edges are defined, then the file should be followed with the header "Vertices" that define each node's state and callback function (that we will soon write ourselves). The format of each line is as such: node name, initial state, and name of callback function. For instance, the first node is v01, with no initial state, and has the callback function with the name sum_product_update_var (defined in the main file below).

This file represents the graph above.


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

Now, let's make our main python file. We start by importing all the necessary packages.


```python
from hmslearn import FactorGraph
import numpy as np
```

Then, in the same file, define all of the callback functions for variable and factor nodes. Make a list containing all update functions.

```python
# helper function for normalizing messages to probability so that the vector sums to 1
def normalize_message(message):
    return message/message.sum() if message.sum() > 0 else np.array([0.5, 0.5])

#callback function for variable nodes
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


#callback function for factor nodes
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

#list of callback functions that will be used
function_list = [variable_node_update_function, factor_node_update_function]
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

Your results should print alongside of the display for redis server, which this package uses. As soon as results are printed, the redis server is closed. 



## Features Being Actively Developed
1. Get asynchronous mode working.
2. Write benchmarks and unit tests for sum and max product.
3. Expand to CUDA.
4. Extend algorithms to gradient descent, classical machine learning, etc.
