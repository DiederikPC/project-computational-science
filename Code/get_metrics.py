import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from SocialGraph import SocialGraph
from SophGraph import SophGraph
import math
from scipy.stats import ks_2samp

# SIGNIFICANCE TEST OF DIFFERENCE IN DIFFERENT METRICS' DISTRIBUTION BETWEEN FB AND BA NETWORK

# GENERAL PARAMETERS
i, i_init, time_steps, decay_rate, sims = 0.01, 0.001, 30, 0.01, 5
threshold = 300

def get_metrics(is_SI, is_BA,i,i_init,time_steps,decay_rate,sims,threshold):

    # THE FOUR METRICS
    perct_list = []
    early_deg = []
    reach_list = []
    speed_list = []

    # USED FOR CALCULATING MSE
    infected_at_t = []


    for iter in range(sims):

        # DEFINE MODEL
        if is_SI:
            graph = SocialGraph(i, i_init, time_steps, "facebook_combined.txt", is_BA)
        else:
            graph = SophGraph(i, i_init, time_steps, decay_rate, "facebook_combined.txt", is_BA)

        for u in range(time_steps):
            graph.make_timestep()

        speed_t = graph.infected_at_t[:np.where((np.absolute(np.array(graph.infected_at_t) - graph.infected_at_t[-1]) < threshold))[0][0]]
        difs = [speed_t[i+1] - speed_t[i] for i in range(len(speed_t)-2)]
        speed_list.append(np.mean(difs))

        if not is_SI:
            reach_list.append(graph.find_furthest_inf_node())

        early_deg.append(np.mean(graph.inf_degree_avg[:10]))
        perct_list.append(graph.inf_count)
        infected_at_t.append(graph.infected_at_t)

    metrics = {'perct_list': perct_list, 'early_deg': early_deg,'reach_list':reach_list,'infected_at_t':infected_at_t,'speed_list':speed_list}
    return metrics

metrics_BA_SI = get_metrics(True,True,i,i_init,time_steps,decay_rate,sims,threshold)

metrics_BA_SI

# GET MSE FROM TWO NETWORKS