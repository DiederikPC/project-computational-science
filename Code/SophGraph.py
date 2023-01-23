from SocialGraph import SocialGraph
import networkx as nx
import numpy as np


class SophGraph(SocialGraph):
    def inf_chance(self, n_neigh, n_inf_neigh):
        """
        Returns the infection chance given number of infected neighbors r
        and global decay rate.
        """
        # probabilities read by eye from the paper we discussed
        probs = [0, 0.014, 0.02, 0.021, 0.021, 0.02, 0.019, 0.018, 0.017,
                 0.016, 0.016, 0.016, 0.015, 0.015, 0.014, 0.014, 0.014,
                 0.013, 0.014]

        # if the number of infected neighbors is larger than 18 we assume
        # stable value of 0.014
        if n_inf_neigh > 18:
            return 0.014 / ((1 + self.decay_rate * self.t) * n_neigh)

        return probs[n_inf_neigh] / ((1 + self.decay_rate * self.t) * n_neigh)


    def __init__(self, edgelist, i, i_init, time_steps, decay_rate):
        super().__init__(edgelist, i, i_init, time_steps)
        self.t = 0
        self.decay_rate = decay_rate

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
                if np.random.uniform() < self.inf_chance(len(neighbors),
                                                         n_inf_neighbors):
                    self.node_states[n] = 1
                    inf_degree.append(total_neighbors)

        nx.set_node_attributes(self.G, self.node_states, "state")

        self.t += 1
        self.update_stats()
        # track average degree of newly infected nodes
        if len(inf_degree) == 0:
            self.inf_degree_avg.append(0)
        else:
            self.inf_degree_avg.append(np.mean(inf_degree))


        return self.inf_count
