import numpy as np

prob_hidden = 0.75
prob_samples = 0.9

x1 = np.random.choice([-1,1], size=1,p=[0.5, 0.5])[0] 
x2 = np.random.choice([x1, -x1], size=1, p=[prob_hidden, 1-prob_hidden])[0]

y1 = np.random.choice([x1, 0, -x1], size=1, p=[prob_samples, (1-prob_samples)/2,
    (1-prob_samples)/2])[0]
y2 = np.random.choice([x2, 0, -x2], size=1, p=[prob_samples, (1-prob_samples)/2,
    (1-prob_samples)/2])[0]

print('x1: ', x1)
print('x2: ', x2)
print('y1: ', y1)
print('y2: ', y2)
