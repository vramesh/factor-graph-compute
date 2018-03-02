import edges, node, state, pubsub


class Factor_Graph:
    def __init__(self, input_path, algorithm):
        self.input_path = input_path
        self.algorithm = algorithm
        self.variable_nodes = list()
        self.factor_nodes = list()
        self.adjacency_dict = dict() # variable to factor

    def read(self, factor_graph_id): # who will keep the factor graph id? I feel like we don't need the id or that problem could manage this by itself
        """ Read the messages of each edge in the final state.

        Returns:
            Dictionary that maps edge objects to their associated values
        """
        pass

    def read_file(self): # We have to make this specific for each algorithm, for example, page rank is adjacency matrix, but stochastic gradient is data points
        if (self.algorithm == "page_rank"): # assume that index is 1,...,n
            adjacency_dict = dict()
            with open(self.input_path) as f:
                all_lines = f.readlines():
                for line in all_lines:
                    [x,y] = line.split()
                    x = int(x)
                    y = int(y)

                    if x in adjacency_dict:
                        adjacency_dict[x].append(y)
                    else:
                        adjacency_dict[x] = [y]

            self.adjacency_dict = adjacency_dict
            self.edges = edges.Edges(self.adjacency_dict)

        else:
            pass

    def update(self, factor_graph_id):
        pass

    def delete(self, factor_graph_id):  # if delete is a method inside the pbject itself, could it delete itself?
        pass

    def terminate(self, factor_graph_id):
        pass

    def run(self, factor_graph_id, terminating_condition):
        
        pass

    
