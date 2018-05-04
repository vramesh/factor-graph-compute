transition_hidden_param = 0.75
observation_param = 0.9

transition_factor_function = lambda input_vector: transition_hidden_param if input_vector[0]==input_vector[1] else 1 - transition_hidden_param 


observation_factor_function = lambda obs, hidden: observation_param if obs==hidden else (1-observation_param)/2 

y1_observation = 1
y2_observation = -1
