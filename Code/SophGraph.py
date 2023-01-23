from SocialGraph import SocialGraph
import networkx as nx
import numpy as np
import random


class SophGraph(SocialGraph):

    def __init__(self, i, i_init, time_steps, decay_rate, edgelist=None,
                 is_barabasi=False):
        super().__init__(i, i_init, time_steps, edgelist=edgelist,
                         is_barabasi=is_barabasi)
        self.t = 1
        self.decay_rate = decay_rate
        self.ave_degree = self.G.number_of_edges() / self.G.number_of_nodes()

    def initialize_cluster(self):
        # set all nodes states to 0
        nodes = self.G.nodes
        self.node_states = dict(zip(nodes, np.zeros(len(nodes))))
        self.update_stats()

        print(sum(self.node_states.values()))
        seed = random.choice([n for n in self.G.nodes])
        cluster_size = self.i_init * len(self.G.nodes)
        while self.inf_count <= cluster_size:

            neighborhood = nx.all_neighbors(self.G, seed)
            for n in nx.all_neighbors(self.G, seed):
                if self.G.nodes[n]["state"] == 0 and self.inf_count <= cluster_size:
                    self.node_states[n] = 1
                    self.update_stats()

            seed = random.choice([n for n in neighborhood])
        print(sum(self.node_states.values()))

    def soph_inf_chance(self, n_neigh, n_inf_neigh, ):
        """
        Returns the infection chance given number of infected neighbors r and
        global decay rate
        """
        # probabilities read by eye from the paper we discussed
        probs = [0, 0.014, 0.02, 0.021, 0.021, 0.02, 0.019, 0.018, 0.017,
                 0.016, 0.016, 0.016, 0.015, 0.015, 0.014, 0.014, 0.014,
                 0.013, 0.014]

        # if the number of infected neighbors is larger than 18 we assume
        # stable value of 0.014
        if n_inf_neigh > 18:
            return ((0.014 * self.ave_degree) /
                    ((1 + self.decay_rate * self.t) * n_neigh))

        return ((probs[n_inf_neigh] * self.ave_degree) /
                ((1 + self.decay_rate * self.t) * n_neigh))

    def make_timestep(self):
        """
            Make a single timestep. Infect new nodes and update statistics.
        """
        inf_degree = []
        for n in self.G.nodes:
            if self.G.nodes[n]["state"] == 0:
                neighbors = nx.all_neighbors(self.G, n)
                neighbor_states = [self.G.nodes[neighbor]['state'] for
                                   neighbor in neighbors]
                n_inf_neighbors = neighbor_states.count(1)
                total_neighbors = len(neighbor_states)

                # newly infected
                if np.random.uniform() < self.soph_inf_chance(total_neighbors,
                                                              n_inf_neighbors):
                    self.node_states[n] = 1
                    inf_degree.append(total_neighbors)

        nx.set_node_attributes(self.G, self.node_states, "state")

        self.update_stats()
        self.current_timestep += 1



fb = SophGraph(0.01, 0.05, 0.01, 50, "../Data/facebook_combined.txt")
fb.initialize_cluster()
fb.draw_graph('start cluster', True)
