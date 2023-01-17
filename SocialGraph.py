import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def inf_chance(r, i):
    """
    Calculates the chance of infection of a node given the total number of
    infected neighbors and the infection rate.
    """
    return 1 - (1-i)**r


class SocialGraph:
    """
        Class to represent a social network
    """
    i = 0.001
    i_init = 0.0001
    time_steps = 1000

    def __init__(self, edgelist):
        self.G = nx.read_edgelist(edgelist, delimiter=' ')
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

    def draw_graph(self, title, show=False):
        """
            Draw the graph, where each infected node is red, each uninfected
            node is blue.
        """
        node_colors = []

        for state in nx.get_node_attributes(self.G, "state").values():
            if state == 1:
                node_colors.append('red')
            else:
                node_colors.append('blue')

        nx.draw(self.G, with_labels=False, node_color=node_colors,
                node_size=20)
        plt.savefig(title + ".png")
        if show:
            plt.show()

    def show_infected_plot(self):
        """
            Plot the amount of infected nodes in a graph.
        """
        plt.figure(figsize=(10, 10))
        plt.plot(list(range(self.time_steps + 1)), self.infected_at_t)
        plt.xlabel("Timestep t")
        plt.ylabel("Amount infected nodes")
        plt.title("Amount of infected nodes at timestep t")
        plt.savefig("infectedplt.png")

    def set_init_values(self, i, i_init):
        self.i = i
        self.i_init = i_init

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
        # track infected and susceptible counts
        self.inf_count = int(np.sum(list(self.node_states.values())))
        self.sus_count = len(self.node_states) - self.inf_count
        self.infected_at_t.append(self.inf_count)
        self.susceptible_at_t.append(self.sus_count)

        # track average degree of newly infected nodes
        self.inf_degree_avg.append(np.mean(inf_degree))

        return self.inf_count


def main():
    FbGraph = SocialGraph('facebook_combined.txt')

    # FbGraph.draw_graph("Before", True)

    for i in range(FbGraph.time_steps):
        print(f"Timestep {i}, infected nodes: {FbGraph.make_timestep()}")

    # FbGraph.draw_graph("After", True)
    FbGraph.show_infected_plot()


if __name__ == "__main__":
    main()