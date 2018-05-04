transition_hidden_param = 0.75
observation_param = 0.9

transition_factor_function = lambda x, y: transition_hidden_param if x==y else 1 - transition_hidden_param 

observation_factor_function = lambda obs, hidden: observation_param if obs==hidden else (1-observation_param)/2 

y1_observation = 1
y2_observation = -1
