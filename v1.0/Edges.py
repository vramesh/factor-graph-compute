class Edges:
    def __init__(self, adjacency_dict):
        self.adjacency_dict = adjacency_dict # assume variable indexed from 1,2,...,v and factor indexed from 1,2,...,f
        self.variable_to_factor = adjacency_dict
        self.factor_to_variable = dict()
        
        for variabel_index in self.variable_to_factor:
            for factor_index in self.variable_to_factor[variabel_index]:
                if factor_index in self.factor_to_variable:
                    self.factor_to_variable[factor_index].append(variabel_index)
                else:
                    self.factor_to_variable[factor_index] = [variabel_index]

    def hh():
