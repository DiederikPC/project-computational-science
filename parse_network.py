import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

i, i_init, time_steps = 0.01, 0.1, 10

def inf_chance(r, i):
    """
    Calculates the chance of infection of a node given the total number of
    infected neighbors and the infection rate.
    """
    return 1 - (1-i)**r

def draw_graph(G):

    node_colors = []

    for state in nx.get_node_attributes(G, 'state').values():
        if state == 1:
            node_colors.append('red')
        else:
            node_colors.append('blue')

    nx.draw(G)
    plt.show()

G = nx.read_edgelist('facebook_combined.txt', delimiter=' ')

nodes = G.nodes()
edges = G.edges()

# # Draw the graph
# nx.draw(G)

# # Show the plot
# plt.show()

# draw_graph(G)

# initialize node states
node_states = {}
for n in range(len(nodes)):
    if np.random.uniform() < i_init:
        # 1 = Infected
        node_states[str(n)] = 1
    else:
        # 0 = Susceptible
        node_states[str(n)] = 0

nx.set_node_attributes(G, node_states, "state")

# initialize infected and susceptible counts
inf = [np.sum(list(node_states.values()))]
sus = [len(node_states) - inf[0]]

# initialize average degree of newly infected nodes
inf_degree_avg = []

# update nodes every time step
for _ in range(time_steps):
    inf_degree = []
    node_states = {}
    for n in G.nodes:
        if G.nodes[n]["state"] == 0:
            neighbors = nx.all_neighbors(G, n)
            neighbor_states = [G.nodes[neighbor]['state'] for neighbor in neighbors]
            n_inf_neighbors = neighbor_states.count(1)
            total_neighbors = len(neighbor_states)

            # newly infected
            if np.random.uniform() < inf_chance(n_inf_neighbors, i):
                node_states[n] = 1
                inf_degree.append(total_neighbors)

            # not infected
            else:
                node_states[n] = 0

        else:
            node_states[n] = 1
    nx.set_node_attributes(G, node_states, "state")

    # track infected and susceptible counts
    cur_inf = np.sum(list(node_states.values()))
    inf.append(cur_inf)
    sus.append(len(node_states) - cur_inf)

    # track average degree of newly infected nodes
    inf_degree_avg.append(np.mean(inf_degree))

print(inf)
print(sus)