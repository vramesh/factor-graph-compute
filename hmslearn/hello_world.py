from package_name import FactorGraph
import time

if __name__ == "__main__":
	config = {
		"algorithm": "hello_world",
		"pubsub_choice": "redis",
		"synchronous": "asynchronous"
	}
	path_to_input_file = "hello_world_fg.txt"

	fg = FactorGraph(path_to_input_file, config)
	fg.run()
	time.sleep(10)
	fg.print_solution()
