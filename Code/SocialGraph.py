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
    def initialize_states(self):
        """
            This is called only in the __init__
        """
        nodes = self.G.nodes()

        # initialize node states
        states = np.zeros(len(nodes))
        states[np.random.uniform(size=len(nodes)) < self.i_init] = 1
        node_states = dict(zip(nodes, states))

        nx.set_node_attributes(self.G, node_states, "state")
        self.inf_count = np.sum(states)
        self.sus_count = len(nodes) - self.inf_count
        self.node_states = node_states
        self.inf_degree_avg = []
        self.infected_at_t = [self.inf_count]
        self.susceptible_at_t = [self.sus_count]

    def __init__(self, i, i_init, time_steps, edgelist=None,
                 is_barabasi=False):
        if edgelist is None and not is_barabasi:
            print("Need to either give and edgelist or set \
                  is_barabasi to true")
            return
        if is_barabasi:
            self.G = nx.barabasi_albert_graph(4039, 20)
        else:
            self.G = nx.read_edgelist("../Data/" + edgelist, delimiter=' ')
            self.pos = None
        self.i = i
        self.i_init = i_init
        self.time_steps = time_steps
        self.edgelist = edgelist
        self.initialize_states()

    def draw_graph(self, title, show=False):
        """
            Draw the graph, where each infected node is red, each uninfected
            node is blue.
        """
        node_colors = []
        if self.pos is None:
            self.pos = nx.spring_layout(self.G)
        for state in nx.get_node_attributes(self.G, "state").values():
            if state == 1:
                node_colors.append('red')
            else:
                node_colors.append('blue')
        print(self.edgelist)

        nx.draw(self.G, self.pos, with_labels=False, node_color=node_colors,
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

    def set_init_values(self, i, i_init):
        self.i = i
        self.i_init = i_init

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

        nx.set_node_attributes(self.G, self.node_states, "state")

        self.update_stats()
        # track average degree of newly infected nodes
        if len(inf_degree) == 0:
            self.inf_degree_avg.append(0)
        else:
            self.inf_degree_avg.append(np.mean(inf_degree))

        return self.inf_count

    def explosiveness(self):
        inf = self.infected_at_t
        explosive_lst = [(inf[x+1]-inf[x])/len(self.nodes) for x in range(len(inf)-1)]
        return explosive_lst

