import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def inf_chance(r, i):
    """
    Calculates the chance of infection of a node given the total number of
    infected neighbors and the infection rate.
    """
    return 1 - (1 - i) ** r


class SocialGraph:
    """
        Class to represent a social network
    """

    def set_init_stats(self):
        """
            Set the initial statistics for the Social Graph.
        """
        self.inf_count = np.sum(list(self.node_states.values()))
        self.sus_count = len(self.G.nodes) - self.inf_count
        self.inf_degree_avg = []
        self.infected_at_t = [self.inf_count]
        self.susceptible_at_t = [self.sus_count]

    def initialize_states(self):
        """
            This is called only in the __init__. It randomly initializes the
            infected node states.
        """
        nodes = self.G.nodes()

        # initialize node states
        states = np.zeros(len(nodes))
        inf_indices = np.random.choice(list(range(4039)),
                                       size=round(self.i_init * len(nodes)))
        for node in inf_indices:
            states[node] = 1

        self.node_states = dict(zip(nodes, states))

        nx.set_node_attributes(self.G, self.node_states, "state")
        self.set_init_stats()

        self.got_infected_at = {}
        for node in self.G.nodes:
            if self.G.nodes[node]['state'] == 1:
                self.got_infected_at[node] = 0

    def __init__(self, i, i_init, time_steps, edgelist=None,
                 is_barabasi=False):
        """
            Initialize the SocialGraph class, including the states and
            statistics.
        """
        if edgelist is None and not is_barabasi:
            print("Need to either give and edgelist or set \
                  is_barabasi to true")
            return
        if is_barabasi:
            self.G = nx.barabasi_albert_graph(4039, 22)
        else:
            self.G = nx.read_edgelist("../Data/" + edgelist, delimiter=' ')
            self.pos = None
            self.edgelist = edgelist

        self.i = i
        self.i_init = i_init
        self.time_steps = time_steps
        self.current_t = 0
        self.initialize_states()

    def draw_graph(self, title, show=False):
        """
            Draw the graph, where each infected node is red, each uninfected
            node is blue.
        """
        node_colors = []
        if self.edgelist is not None and self.pos is None:
            self.pos = nx.spring_layout(self.G)

        for state in nx.get_node_attributes(self.G, "state").values():
            if state == 1:
                node_colors.append('red')
            else:
                node_colors.append('blue')

        print(self.edgelist)
        if self.edgelist is not None:
            nx.draw(self.G, self.pos, with_labels=False,
                    node_color=node_colors, node_size=20)
        else:
            nx.draw(self.G, with_labels=False, node_color=node_colors,
                    node_size=20)

        plt.savefig("../Plots/" + title + ".png")

        if show:
            plt.show()
        plt.close()

    def show_infected_plot(self, title):
        """
            Plot the amount of infected nodes in a graph.
        """
        # normalize number of infected nodes
        infected_at_t_percent = [i / len(self.G.nodes)
                                 for i in self.infected_at_t]
        plt.figure(figsize=(10, 10))
        plt.plot(list(range(self.time_steps + 1)), infected_at_t_percent)
        plt.xlabel("Timestep t")
        plt.ylabel("Amount infected nodes")
        plt.title("Amount of infected nodes at timestep t")
        plt.savefig("../Plots/" + title)
        plt.close()

    def update_stats(self):
        """
        Update the statistics that change with each timestep.
        """
        # track infected and susceptible counts
        self.inf_count = int(np.sum(list(self.node_states.values())))
        self.sus_count = len(self.node_states) - self.inf_count
        self.infected_at_t.append(self.inf_count)
        self.susceptible_at_t.append(self.sus_count)

    def make_timestep(self):
        """
            Make a single timestep. Infect new nodes and update statistics.
        """
        self.current_t += 1

        inf_degree = []
        for n in self.G.nodes:
            if self.G.nodes[n]["state"] == 0:
                neighbors = nx.all_neighbors(self.G, n)
                neighbor_states = [self.G.nodes[neighbor]['state'] for
                                   neighbor in neighbors]
                n_inf_neighbors = neighbor_states.count(1)
                total_neighbors = len(neighbor_states)

                # newly infected
                if np.random.uniform() < inf_chance(n_inf_neighbors,
                                                    self.i):
                    self.node_states[n] = 1
                    inf_degree.append(total_neighbors)
                    self.got_infected_at[n] = self.current_t

        nx.set_node_attributes(self.G, self.node_states, "state")

        self.update_stats()
        # track average degree of newly infected nodes
        if len(inf_degree) == 0:
            self.inf_degree_avg.append(0)
        else:
            self.inf_degree_avg.append(np.mean(inf_degree))

        return self.inf_count

    def calculate_explosiveness(self):
        """
            Calculates the percentage of the network that gets infected each
            timestep
        """
        inf = self.infected_at_t
        explosive_lst = [(inf[x + 1] - inf[x]) / len(self.G.nodes())
                         for x in range(len(inf) - 1)]
        return explosive_lst

    def get_influential_nodes(self, visualize=False):
        """
            Get the most influential nodes in the network.
        """
        # calculate node centralities
        degree_centrality = nx.degree_centrality(self.G)
        sorted_degree = sorted(degree_centrality.items(),
                               key=lambda x: x[1], reverse=True)

        betweenness_centrality = nx.betweenness_centrality(self.G)
        sorted_betweenness = sorted(betweenness_centrality.items(),
                                    key=lambda x: x[1], reverse=True)

        closeness_centrality = nx.closeness_centrality(self.G)
        sorted_closeness = sorted(closeness_centrality.items(),
                                  key=lambda x: x[1], reverse=True)

        # calculate individual node influence scores (the lower the better)
        centralities = [sorted_degree, sorted_betweenness, sorted_closeness]
        centrality_scores = {str(node): 0 for node in self.G.nodes()}

        for centrality in centralities:
            for i, (node, _) in enumerate(centrality):
                centrality_scores[str(node)] += i

        centrality_scores = sorted(centrality_scores.items(),
                                   key=lambda x: x[1])

        # get most influential nodes with cutoff point (100)
        most_inf_nodes = [node for (node, score) in centrality_scores if
                          score <= 100]
        self.most_inf_nodes = most_inf_nodes
        print(f'Most influential nodes as a combination of degree, betweenness\
               and closeness centrality:\n{most_inf_nodes}')

        # visualize influential nodes
        if visualize:
            colors = []
            size = []
            for node in self.G.nodes():
                if str(node) in most_inf_nodes:
                    colors.append('red')
                    size.append(100)
                else:
                    colors.append('blue')
                    size.append(2)

            nx.draw(self.G, with_labels=False, node_color=colors,
                    node_size=size)
            plt.show()

        return most_inf_nodes
