import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

N, i, i_init, time_steps = 10**5, 0.01, 0.1, 200

s = nx.utils.powerlaw_sequence(100000, 2.5)
s = s / np.mean(s) * 5
G = nx.expected_degree_graph(s, selfloops=False)

#########

def inf_chance(r, i):
    """
    Calculates the chance of infection of a node given the total number of
    infected neighbors and the infection rate.
    """
    return 1 - (1-i)**r


G = nx.read_edgelist('facebook_combined.txt', delimiter=' ')

nodes = G.nodes()
edges = G.edges()

# # Draw the graph
# nx.draw(G)

# # Show the plot
# plt.show()

# initialize node states
node_states = {}
for n in range(len(nodes)):
    if np.random.uniform() < i_init:
        # 1 = Infected
        node_states[n] = 1
    else:
        # 0 = Susceptible
        node_states[n] = 0

# print(node_states)
nx.set_node_attributes(G, node_states, "state")

# initialize infected and susceptible counts
inf = [np.sum(list(node_states.values()))]
sus = [len(node_states) - inf[0]]

# initialize average degree of newly infected nodes
inf_degree_avg = []
print(f"node 0: {node_states[0]}")
# update nodes every time step
for _ in range(time_steps):
    inf_degree = []
    node_states = {}
    for n in G.nodes:
        print(n)
        if node_states[0] == 0:
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