from SocialGraph import SocialGraph
import networkx as nx
import numpy as np


class SophGraph(SocialGraph):
    """
        A class to represent a more sophisticated network than the SocialGraph
        class, the improvements are based on empirical data. Some of them are:
            - A decay rate, which 'ages' an idea, making it less likely to
                spread during later timesteps
            - Clustering the initial nodes instead of picking random nodes
                through the network
            - Taking the spread probability from previous research, instead
                of setting it ourselves.
    """
    def __init__(self, i, i_init, time_steps, decay_rate, edgelist=None,
                 is_barabasi=False):
        """
            Initialize the SophGraph class, mostly by calling the socialgraph.
        """
        super().__init__(i, i_init, time_steps, edgelist=edgelist,
                         is_barabasi=is_barabasi)
        self.t = 1

        self.decay_rate = decay_rate
        self.ave_degree = self.G.number_of_edges() / self.G.number_of_nodes()
        self.initialize_cluster()

    def initialize_cluster(self):
        """
            Picks a random node and infects it and its neighbourhood. If that
            does not infect a sufficient amount of nodes (set by i_init), it
            picks one of the neighbours and infects that neighbourhood.
        """
        # set all nodes states to 0
        nodes = self.G.nodes
        self.node_states = dict(zip(nodes, np.zeros(len(nodes))))

        seed = np.random.choice(list(nodes))
        self.seed = seed
        self.node_states[seed] = 1
        cluster_size = self.i_init * len(nodes)

        while self.inf_count <= cluster_size:
            neighborhood = nx.all_neighbors(self.G, seed)
            for n in nx.all_neighbors(self.G, seed):
                if nodes[n]["state"] == 0 and self.inf_count <= cluster_size:
                    self.node_states[n] = 1
                    self.update_stats()

            seed = np.random.choice(list(neighborhood))
        nx.set_node_attributes(self.G, self.node_states, "state")
        self.set_init_stats()

    def soph_inf_chance(self, n_neigh, n_inf_neigh, ):
        """
        Returns the infection chance given number of infected neighbors r and
        global decay rate.
        """
        # Probabilities read by eye from the paper we discussed
        probs = [0, 0.014, 0.02, 0.021, 0.021, 0.02, 0.019, 0.018, 0.017,
                 0.016, 0.016, 0.016, 0.015, 0.015, 0.014, 0.014, 0.014,
                 0.013, 0.014]

        # If the number of infected neighbors is larger than 18 we assume
        # stable value of 0.014
        if n_inf_neigh > 18:
            return self.i * ((0.014 * self.ave_degree) /
                             ((1 + self.decay_rate * self.t) * n_neigh))

        return self.i * ((probs[n_inf_neigh] * self.ave_degree) /
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
        self.t += 1

        if len(inf_degree) == 0:
            self.inf_degree_avg.append(0)
        else:
            self.inf_degree_avg.append(np.mean(inf_degree))

        return self.inf_count

    def determine_reach(self):
        """
            Determines the length of the shortest distance between the furthest
            infected node and the very first infected node. **Not used for the
            research**
        """
        longest = 0
        nodes = np.array(list(self.G.nodes))
        values = np.array(list(nx.get_node_attributes(self.G,
                                                      "state").values()))
        copyG = self.G.copy()
        for node in nodes[np.where(values == 0)]:
            copyG.remove_node(node)

        longest = list((nx.single_source_shortest_path_length(copyG,
                                                              self.seed)).
                       values())[-1]
        return longest
