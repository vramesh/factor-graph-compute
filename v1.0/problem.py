import json
from factor_graph import FactorGraph, FactorGraphService


class Problem:
    def __init__(self):
        pass

    def solve(self, path_to_input_file, config_path = "default_config.json"): #get back to config
        with open(config_path, "r") as f:
            config = json.load(f)

        # Check all necessary configuration
        necessary_config = ["algorithm", "synchronuos", "pubsub_choice"]
        for attribute in necessary_config:
            if attribute not in config:
                raise ValueError("config file needs " + attribute)

        factor_graph = FactorGraphService.create(path_to_input_file, config)
        answer_dictionary = FactorGraphService.run(factor_graph)
        return answer_dictionary

