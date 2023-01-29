import numpy as np
import matplotlib.pyplot as plt
from get_metrics import get_metrics
import pandas as pd

def get_param_results(parameter, parameter_range, is_SI):
    sims = 5
    threshold = 30
    params = {"i": 0.01, "i_init": 0.001, "time_steps": 30, "decay_rate": 0.1}
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
            FB_results[name].append(np.mean(FB[name]))
            BA_results[name].append(np.mean(BA[name]))

    data = pd.DataFrame({'i': parameter_range,
                        'infec_list_FB': FB_results['infec_list'],
                        'infec_list_BA': BA_results['infec_list'],
                        'early_deg_FB': FB_results['early_deg'],
                        'early_deg_BA': BA_results['early_deg'],
                        'speed_list_FB': FB_results['speed_list'],
                        'speed_list_BA': BA_results['speed_list']})
    
    model = 'SI' if is_SI else 'Soph'
    data.to_csv(f'../Data/Results/results_{model}_{parameter}.csv', index=False)




