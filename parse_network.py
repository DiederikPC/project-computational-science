import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

i, i_init, time_steps = 0.01, 0.1, 10

def inf_chance(r, i):
    """
    Calculates the chance of infection of a node given the total number of
    infected neighbors and the infection rate.
    """
    return 1 - (1-i)**r


def draw_graph(G, title):

    node_colors = []

    for state in nx.get_node_attributes(G, "state").values():
        if state == 1:
            node_colors.append('red')
        else:
            node_colors.append('blue')

    nx.draw(G, with_labels=False, node_color=node_colors, node_size=20)
    plt.savefig(title + ".png")
    plt.show()


def initialize_graph():
    G = nx.read_edgelist('facebook_combined.txt', delimiter=' ')

    nodes = G.nodes()

    # initialize node states
    infected = np.zeros(len(nodes))
    infected[np.random.uniform(size = len(nodes)) < i_init] = 1
    node_states = dict(zip(nodes, infected))

    nx.set_node_attributes(G, node_states, "state")

    return G


def make_timestep():
    inf_degree = []
    node_states = {}
    for n in G.nodes:
        if G.nodes[n]["state"] == 0:
            neighbors = nx.all_neighbors(G, n)
            neighbor_states = [G.nodes[neighbor]['state'] for
                               neighbor in neighbors]
            n_inf_neighbors = neighbor_states.count(1)
            total_neighbors = len(neighbor_states)

            # newly infected
            if np.random.uniform() < inf_chance(n_inf_neighbors, i):
                node_states[n] = 1
                inf_degree.append(total_neighbors)

    nx.set_node_attributes(G, node_states, "state")

    # track infected and susceptible counts
    cur_inf = np.sum(list(node_states.values()))
    inf.append(cur_inf)
    sus.append(len(node_states) - cur_inf)

    # track average degree of newly infected nodes
    inf_degree_avg.append(np.mean(inf_degree))

# initialize infected and susceptible counts
# inf = [np.sum(list(node_states.values()))]
# sus = [len(node_states) - inf[0]]

# initialize average degree of newly infected nodes
inf_degree_avg = []

G = initialize_graph()
print(nx.get_node_attributes(G, "state"))
make_timestep()
print()
# # update nodes every time step
# for _ in range(time_steps):
#     make_timestep(G)


# print(inf)
# print(sus)