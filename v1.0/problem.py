import factor_graph

class Problem:
    def __init__(self):
        self.current_factor_graph_id = 0
        self.all_running_factor_graph = dict()

    # def solve(self, path_to_file, config):
    #     pass
    
    # Need to be added as inputs, synchro_mode, pubsub_choice, pubsub_heuristic
    def solve(self, path_to_fg_states, output_path, algorithm="page_rank"):
        print "Optimization id" + str(self.current_factor_graph_id)
        main_factor_graph = Factor_graph(path_to_fg_states, algorithm)
        all_running_factor_graph[self.current_factor_graph_id] = main_factor_graph
        self.current_factor_graph_id += 1

    def delete(self, factor_graph_id):
        pass

