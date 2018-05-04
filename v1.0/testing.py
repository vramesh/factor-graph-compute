import inspect
import user_input_functions
import argparse

all_functions = inspect.getmembers(user_input_functions, inspect.isfunction)

func_dict = dict()
for function_tuple in all_functions:
	func_dict[function_tuple[0]] = function_tuple[1]
print(func_dict)

'''
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("functions", type=str)
args = parser.parse_args()
file = args.file
functions_file = args.functions
'''





