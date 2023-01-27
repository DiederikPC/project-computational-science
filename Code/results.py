import numpy as np
import matplotlib.pyplot as plt
from get_metrics import get_metrics
import pandas as pd


i, i_init, time_steps, decay_rate, sims = 0.01, 0.001, 30, 0.01, 2
threshold = 30

parameter_range = np.linspace(0, 0.5, 3)
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

data = pd.DataFrame(SI_BA_results)
data.insert(0, "i", parameter_range)
data.to_csv('..GfG.csv',)



# plt.figure()
# plt.plot(parameter_range, SI_FB_results['speed_list'], label='FB')
# plt.plot(parameter_range, SI_BA_results['speed_list'], label='BA')
# plt.legend()
# plt.show()



