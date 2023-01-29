import numpy as np
import matplotlib.pyplot as plt
from get_metrics import get_metrics
import pandas as pd

# PARAMETER i
i, i_init, time_steps, decay_rate, sims = 0.01, 0.001, 30, 0.1, 15
threshold = 30
parameter_range = np.linspace(0, 0.5, 20)
metric_names = ['infec_list', 'early_deg', 'speed_list']
SI_FB_results = {'infec_list': [], 'early_deg': [], 'speed_list': []}
SI_BA_results = {'infec_list': [], 'early_deg': [], 'speed_list': []}

for i in parameter_range:
    print(i)
    SI_FB = get_metrics(True, False, i, i_init, time_steps, decay_rate, sims,
                        threshold)
    SI_BA = get_metrics(True, True, i, i_init, time_steps, decay_rate, sims,
                        threshold)
    for name in metric_names:
        SI_FB_results[name].append(np.mean(SI_FB[name]))
        SI_BA_results[name].append(np.mean(SI_BA[name]))

data = pd.DataFrame({'i': parameter_range, 'infec_list_FB': SI_FB_results['infec_list'],
                     'infec_list_BA': SI_BA_results['infec_list'], 'early_deg_FB': SI_FB_results['early_deg'],
                     'early_deg_BA': SI_BA_results['early_deg'], 'speed_list_FB': SI_FB_results['speed_list'],
                     'speed_list_BA': SI_BA_results['speed_list']})

data.to_csv('../Data/Results/results_SI_I.csv', index=False)




