from SocialGraph import SocialGraph
import networkx as nx
import numpy as np


def soph_inf_chance(n_neigh, n_inf_neigh, global_decay, time_step, ave_degree):
    """
    Returns the infection chance given number of infected neighbors r and global decay rate
    """
    # probabilities read by eye from the paper we discussed
    probs = [0, 0.014, 0.02, 0.021, 0.021, 0.02, 0.019, 0.018, 0.017, 0.016, 0.016, 0.016, 0.015, 0.015, 0.014, 0.014,
             0.014, 0.013, 0.014]

    # if the number of infected neighbors is larger than 18 we assume stable value of 0.014
    if n_inf_neigh > 18:
        return (0.014 * ave_degree) / ((1 + global_decay * time_step) * n_neigh)

    return (probs[n_inf_neigh] * ave_degree) / ((1 + global_decay * time_step) * n_neigh)


class SophGraph(SocialGraph):
    def __init__(self, edgelist, global_decay, i_init, time_steps):
        self.G = nx.read_edgelist("../Data/" + edgelist, delimiter=' ')
        self.i_init = i_init
        self.time_steps = time_steps
        self.edgelist = edgelist
        self.initialize_states()

        self.global_decay = global_decay
        self.current_timestep = 1

        self.ave_degree = self.G.number_of_edges() / self.G.number_of_nodes()

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
                if np.random.uniform() < soph_inf_chance(total_neighbors, n_inf_neighbors, self.global_decay,
                                                         self.current_timestep, self.ave_degree):
                    self.node_states[n] = 1
                    inf_degree.append(total_neighbors)

        nx.set_node_attributes(self.G, self.node_states, "state")

        self.update_stats()
        self.current_timestep += 1

