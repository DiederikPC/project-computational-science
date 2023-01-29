import numpy as np
import math
from SocialGraph import SocialGraph
from SophGraph import SophGraph


# SIGNIFICANCE TEST OF DIFFERENCE IN DIFFERENT METRICS' DISTRIBUTION BETWEEN FB
# AND BA NETWORK

# GENERAL PARAMETERS
i, i_init, time_steps, decay_rate, sims = 0.01, 0.001, 30, 0.01, 5
threshold = 300


def get_metrics(is_SI, is_BA, i, i_init, time_steps, decay_rate, sims,
                threshold):

    # THE FOUR METRICS
    infec_list = []
    early_deg = []
    reach_list = []
    speed_list = []

    # USED FOR CALCULATING MSE
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
        mean_speed = np.mean(difs)
        speed_list.append(mean_speed)

        # if not is_SI:
        #     reach_list.append(graph.determine_reach())

        early_deg.append(np.mean(graph.inf_degree_avg[:10]))
        infec_list.append(graph.inf_count)
        infected_at_t.append(graph.infected_at_t)

    metrics = {'infec_list': infec_list, 'early_deg': early_deg,
               'reach_list': reach_list, 'infected_at_t': infected_at_t,
               'speed_list': speed_list}
    return metrics

# function to get average error percentage
def average_error_percent(FB, BA):
    """
    Returns the average percentage difference between Facebook and
    Barabasi-Albert values. Arguments are a list for a metric for FB and a list
    for the same metric for BA
    """
    return np.mean((np.abs(np.array(BA) - np.array(FB)) / np.array(BA)))

# average_error_percent(SI_FB_results['speed_list'], SI_BA_results['speed_list'])
