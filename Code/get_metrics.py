# FUNCTIONS USED IN RUNNING_MODEL.PY AND VISUALIZE_&_RESULTS.PY
import numpy as np
from SocialGraph import SocialGraph
from SophGraph import SophGraph
import pandas as pd

def get_metrics(is_SI, is_BA, i, i_init, time_steps, decay_rate, sims,
                threshold):
    """ 
    For a given network and model, and provided its parameter values, runs the model n=sims times
    and stores relevant metrics (reach, speed and avg. degree of early infected nodes) for each
    of the simulations. 
    """
    infec_list = []
    early_deg = []
    speed_list = []

    infected_at_t = []

    for iter in range(sims):
        print("Current sim:", iter)

        # DEFINE MODEL
        if is_SI:
            graph = SocialGraph(i, i_init, time_steps,
                                "facebook_combined.txt", is_BA)
        else:
            graph = SophGraph(i, i_init, time_steps, decay_rate,
                              "facebook_combined.txt", is_BA)

        for u in range(time_steps):
            graph.make_timestep()

        inf_diff = np.absolute(np.array(graph.infected_at_t) -
                               graph.infected_at_t[-1]) < threshold
        speed_t = graph.infected_at_t[:np.where(inf_diff)[0][0]]
        difs = [speed_t[i+1] - speed_t[i] for i in range(len(speed_t) - 2)]

        # On the off chance no new nodes get infected during the entire
        # simulation the average speed is set to zero
        if not difs:
            difs = [0]

        mean_speed = np.mean(difs)
        speed_list.append(mean_speed)

        early_deg.append(np.mean(graph.inf_degree_avg[:10]))
        infec_list.append(graph.inf_count)
        infected_at_t.append(graph.infected_at_t)

    metrics = {'infec_list': infec_list, 'early_deg': early_deg,'infected_at_t': infected_at_t,
               'speed_list': speed_list}
    return metrics

def get_param_results(parameter, parameter_range, is_SI):
    """
    For a given parameter and over a given range of values of this parameter, runs get_metrics on both 
    the BA and FB networks at each of the values of the parameters and stores given metrics as csv file in Data/Results. 
    """
    sims = 20
    threshold = 30
    params = {"i": 0.01, "i_init": 0.001, "time_steps": 30, "decay_rate": 0.1}
    if not is_SI:
        params['i'] = 1
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

    raw_index = [np.repeat(round(x, 4), sims) for x in parameter_range]
    index = [elem for sublist in raw_index for elem in sublist]
    print(FB_results)
    data = pd.DataFrame({f'{parameter}': index,
                        'infec_list_FB': FB_results['infec_list'],
                         'infec_list_BA': BA_results['infec_list'],
                         'early_deg_FB': FB_results['early_deg'],
                         'early_deg_BA': BA_results['early_deg'],
                         'speed_list_FB': FB_results['speed_list'],
                         'speed_list_BA': BA_results['speed_list']})

    model = 'SI' if is_SI else 'Soph'
    data.to_csv(f'../Data/Results/results_{model}_{parameter}.csv',
                index=False)

def average_error_percent(FB, BA):
    """
    Returns the average percentage difference between Facebook and
    Barabasi-Albert values for a given metric. Arguments are a list for a metric for FB and a list
    for the same metric for BA
    """
    return 100*np.mean((np.abs(np.array(BA) - np.array(FB)) / np.array(BA)))


