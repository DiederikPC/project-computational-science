from SocialGraph import SocialGraph
import networkx as nx
import numpy as np

def soph_inf_chance(n_neigh, n_inf_neigh, global_decay, time_step):
    """
    Returns the infection chance given number of infected neighbors r and global decay rate
    """
    # probabilities read by eye from the paper we discussed
    probs = [0, 0.014, 0.02, 0.021, 0.021, 0.02, 0.019, 0.018, 0.017, 0.016, 0.016, 0.016, 0.015, 0.015, 0.014, 0.014,
             0.014, 0.013, 0.014]

    # if the number of infected neighbors is larger than 18 we assume stable value of 0.014
    if n_inf_neigh > 18:
        return 0.014 / ((1 + global_decay * time_step) * n_neigh)

    return probs[n_inf_neigh] / ((1 + global_decay * time_step) * n_neigh)


class SophGraph(SocialGraph):
    def __init__(self, edgelist, i, i_init, time_steps):
        super().__init__(edgelist, i, i_init, time_steps)

    def make_timestep(self):
        super().make_timestep()

