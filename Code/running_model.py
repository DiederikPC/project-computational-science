import numpy as np
from get_metrics import get_param_results

steps = 20
parameters = ['i', 'i_init', 'decay_rate']
parameters_range = [np.linspace(0.5, 2.5, steps),
                    np.linspace(0.01, 0.21, steps),
                    np.linspace(0.01, 0.21, steps)]
models = [False, False, False]

for i in range(len(parameters)):
    get_param_results(parameters[i], parameters_range[i], models[i])
