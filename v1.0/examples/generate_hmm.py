import numpy as np
from hmm_factor_functions import transition_hidden_param, observation_param

def generate_hmm(transition_hidden_param=0.75, observation_param=0.9):
    x1 = np.random.choice([-1,1], size=1,p=[0.5, 0.5])[0] 

    x2 = np.random.choice([x1, -x1], size=1, p=[transition_hidden_param,
        1-transition_hidden_param])[0]

    y1 = np.random.choice([x1, 0, -x1], size=1, p=[observation_param,
        (1-observation_param)/2,
        (1-observation_param)/2])[0]

    y2 = np.random.choice([x2, 0, -x2], size=1, p=[observation_param,
        (1-observation_param)/2,
        (1-observation_param)/2])[0]
    return {'x1': x1,
            'x2': x2,
            'y1': y1,
            'y2': y2}

if __name__ == '__main__':
    hmm = generate_hmm()
    with open('hmm_factor_graph.txt', 'w+') as f:
        for variable, value in hmm.items():
            f.write(
            print(variable, ':', value)



