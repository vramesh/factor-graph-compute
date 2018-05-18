To install this packge, run pip install package_name.

Before running anything, make sure you have Redis installed and running on your computer by running the terminal command 

redis-server


To do hello world example:
Create a factor graph file called `hello_world_two_node_fg.txt` with contents:
```
Edges
v0 f0 None
f0 v0 None
Vertices
v0 Andy update_var_hello_world
f0 None update_fac_hello_world
```

Now create a file called `hello_world.py` with contents:
```
def update_var_hello_world(four arguments):
	print("hello world", name)

def update_fac_hello_world(four arguments):
	print("bye world")
```

To Run:
Option 1:
create a file called `hello_world.py` with the following contents:
```
from package_name import FactorGraph
import time

if __name__ == "__main__":
	config = {
		"algorithm_file_name": "hello_world.py",
		"pubsub_choice": "redis",
		"synchronous": "asynchronous"
	}
	path_to_input_file = "hello_world_fg.txt"

	fg = FactorGraph(path_to_input_file, config)
	fg.run()
	time.sleep(10)
	fg.print_solution()
```

Now run:
`pipenv python hello_world.py`

Option 2:
Create a file called `redis_factor_graph.py` with contents:
`pipenv python factor_graph -i hello_world_fg -p redis -s async -a hello_world`
(need to handle case of being able to run user defined algorithm and able to run one of our default algorithms)

Demo for Tues:
demo option 2 w/ user defined function (hello world)
demo option 2 w/ default defined function (pagerank)