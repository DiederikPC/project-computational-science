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

def get_metrics(is_SI, is_BA,i,i_init,time_steps,decay_rate,sims):
    perct_list = []
    early_deg = []

    for iter in range(sims):

        # DEFINE MODEL 
        if is_SI:
            graph = SocialGraph(i, i_init, time_steps, "facebook_combined.txt", is_BA)
        else:
            graph = SophGraph(i, i_init, time_steps, decay_rate, "facebook_combined.txt", is_BA)

        for u in range(time_steps):
            graph.make_timestep()
        
        early_deg.append(np.mean(graph.inf_degree_avg[:10]))
        perct_list.append(graph.inf_count)


    metrics = {'perct_list': perct_list, 'early_deg': early_deg}
    return metrics

metrics_BA_SI = get_metrics(True,True,i,i_init,time_steps,decay_rate,sims)