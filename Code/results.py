import numpy as np
import matplotlib.pyplot as plt
from get_metrics import get_metrics
import pandas as pd


# function to get all metrics for a model as a parameter changes
def get_param_results(parameter, parameter_range, is_SI):
    sims = 20
    threshold = 30
    params = {"i": 0.01, "i_init": 0.001, "time_steps": 30, "decay_rate": 0.1}
    if not is_SI: 
        params['i'] = 1
    if parameter == 'decay':
        params['i_init'] = 0.06
    metric_names = ['infec_list', 'early_deg', 'speed_list']
    FB_results = {'infec_list': [], 'early_deg': [], 'speed_list': []}
    BA_results = {'infec_list': [], 'early_deg': [], 'speed_list': []}

    for j in parameter_range:
        params[parameter] = j
        print(f"parameter: {parameter}, value: {j}")
        FB = get_metrics(is_SI, False, params["i"], params["i_init"],
                            params["time_steps"], params["decay_rate"], sims,
                            threshold)
        BA = get_metrics(is_SI, True, params["i"], params["i_init"],
                            params["time_steps"], params["decay_rate"], sims,
                            threshold)
        for name in metric_names:
            FB_results[name] = FB_results[name] + FB[name]
            BA_results[name] = BA_results[name] + BA[name]

    raw_index = [np.repeat(round(x,4),sims) for x in parameter_range]
    index = [elem for sublist in raw_index for elem in sublist]

    data = pd.DataFrame({f'{parameter}': index,
                        'infec_list_FB': FB_results['infec_list'],
                        'infec_list_BA': BA_results['infec_list'],
                        'early_deg_FB': FB_results['early_deg'],
                        'early_deg_BA': BA_results['early_deg'],
                        'speed_list_FB': FB_results['speed_list'],
                        'speed_list_BA': BA_results['speed_list']})
    
    model = 'SI' if is_SI else 'Soph'
    data.to_csv(f'../Data/Results/results_{model}_{parameter}.csv', index=False)


steps = 20
parameters = ['i','i_init','i','i_init','decay']
parameters_range = [np.linspace(0,0.042,steps),np.linspace(0,0.03,steps),np.linspace(0.5,2.5,steps),
                np.linspace(0.01,0.21,steps),np.linspace(0.01,0.41,steps)]
models = [True, True, False, False, False]

for i in range(len(parameters)):
    get_param_results(parameters[i],parameters_range[i],models[i])



