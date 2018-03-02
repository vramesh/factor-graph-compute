from factor_graph import FactorGraph, FactorGraphService



class Problem:
	def __init__(self):
		pass

	def solve(self, path_to_file, config={}): #get back to config
		factor_graph = FactorGraphService.create(path_to_file, config)
		answer_dictionary = FactorGraphService.run(factor_graph)
		return answer_dictionary
