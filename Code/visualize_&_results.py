import numpy as np
import matplotlib.pyplot as plt
from get_metrics import average_error_percent
import pandas as pd


# VISUALIZATION
def get_graph(parameter, model):
    """
        Visualize the measured metrics for the given parameter and model
        in a graph.
    """
    raw_data = pd.read_csv(fr'../Data/Results/results_{model}_{parameter}.csv')

    raw_data['infec_list_FB'] = np.array(raw_data['infec_list_FB'])/4039
    raw_data['infec_list_BA'] = np.array(raw_data['infec_list_BA'])/4039

    data_m = raw_data.groupby(by=parameter, as_index=False).mean()
    data_sd = raw_data.groupby(by=parameter, as_index=False).std()

    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f'model: {model}, parameter: {parameter}')

    first_axis = [0, 0, 1, 1]
    second_axis = [0, 1, 0, 1]
    for_fb = [1, 3, 5]
    for_ba = [2, 4, 6]
    title = ['proportion infected', 'early_deg', 'speed of infection']

    for i in range(3):

        fb_mean = np.array(data_m.iloc[:, for_fb[i]])
        fb_error = np.array(data_sd.iloc[:, for_fb[i]]) * 1.96
        ba_mean = np.array(data_m.iloc[:, for_ba[i]])
        ba_error = np.array(data_sd.iloc[:, for_ba[i]]) * 1.96

        axs[first_axis[i], second_axis[i]].plot(data_m.iloc[:, 0],
                                                fb_mean, label='FB',
                                                color='blue')
        axs[first_axis[i], second_axis[i]].plot(data_m.iloc[:, 0],
                                                ba_mean, label='BA',
                                                color='brown')

        axs[first_axis[i], second_axis[i]].fill_between(data_m.iloc[:, 0],
                                                        fb_mean + fb_error,
                                                        fb_mean - fb_error,
                                                        alpha=0.2,
                                                        edgecolor='blue')
        axs[first_axis[i], second_axis[i]].fill_between(data_m.iloc[:, 0],
                                                        ba_mean + ba_error,
                                                        ba_mean - ba_error,
                                                        alpha=0.2,
                                                        color='brown',
                                                        edgecolor='brown')
        axs[first_axis[i], second_axis[i]].set_ylabel(title[i])

    axs[0, 0].legend()
    plt.savefig("../image.png")
    plt.show()


get_graph('decay_rate', 'Soph')

# AVERAGE ERROR PERCENT
results = pd.DataFrame({'model': [], 'parameter': [], 'metric': [],
                        'avg_perc_error': []})

models = ['SI', 'Soph']
parameters_SI = ['i', 'i_init']
parameters_Soph = ['i', 'i_init', 'decay_rate']
metrics = ['infec', 'early_deg', 'speed']

for mod in models:
    if mod == 'SI':
        parameters = parameters_SI
    else:
        parameters = parameters_Soph
    for par in parameters:
        raw_data = pd.read_csv(fr'../Data/Results/results_{mod}_{par}.csv')
        c_raw_data = raw_data[raw_data[par] != 0]
        data_m = c_raw_data.groupby(par).mean()
        i = 0
        for met in metrics:
            avg = average_error_percent(data_m.iloc[:, i], data_m.iloc[:, i+1])
            i += 2
            results.loc[len(results.index)] = [mod, par, met, avg]
