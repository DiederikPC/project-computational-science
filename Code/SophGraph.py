from SocialGraph import SocialGraph
import networkx as nx
import numpy as np

class SophGraph(SocialGraph):
    def __init__(self, edgelist, i, i_init, time_steps):
        super().__init__(edgelist, i, i_init, time_steps)

    def make_timestep(self):
        super().make_timestep()

