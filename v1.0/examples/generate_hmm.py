import numpy as np
from graphical_model import HiddenMarkovModel

if __name__ == '__main__':
    hidden_param = 0.75
    sample_param = 0.9
    num_variables = 2
    hidden_transition_probability_matrix = np.array([[hidden_param,
        1-hidden_param], [1-hidden_param, hidden_param]])
    sample_probability_matrix = np.array([[sample_param, (1-sample_param)/2,
        (1-sample_param)/2], [(1-sample_param)/2, (1-sample_param)/2,
            sample_param]]).T
    
    initial_variable_probability = np.array([0.5, 0.5])
    hidden_alphabet = [-1, 1] 
    sample_alphabet = [-1, 0, 1] 

    hmm = HiddenMarkovModel(num_variables, hidden_transition_probability_matrix,
            sample_probability_matrix, initial_variable_probability,
            hidden_alphabet, sample_alphabet)
    observations = hmm.generate_observations()
    print('observations', observations)
    hmm.convert_to_factor_graph_old(observations, 'test_hmm_conversion')

