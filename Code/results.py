import numpy as np
import matplotlib.pyplot as plt
from get_metrics import get_param_results
import pandas as pd

parameters = ['i','i_init','i','i_init','decay']
parameters_range = [np.arange(0.1,0.21,0.01),np.arange(0.1,0.21,0.01),np.arange(0.5,2.5,0.1),
                np.arange(0.1,0.21,0.01),np.arange(0.1,0.21,0.01)]
models = [True, True, False, False, False]

for i in range(len(parameters)):
    get_param_results(parameters[i],parameters_range[i],model = models[i])




