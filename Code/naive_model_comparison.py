import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from SocialGraph import SocialGraph


sims, i, i_init, time_steps = 500, 0.01, 0.1, 50

# open the facebook and barabasi-albert networks
facebook = SocialGraph("../Data/facebook_combined.txt", i, i_init, time_steps)
BA = SocialGraph("../Data/barabasi_albert.txt", i, i_init, time_steps)


def refresh_BA():
    """
    Generates a BA graph and stores the edge information into a textfile.
    """
    graph = nx.barabasi_albert_graph(4039, 22)
    with open('../Data/barabasi_albert.txt', 'w') as f:
        for edge in graph.edges():
            f.write(str(edge[0]) + " " + str(edge[1]) + "\n")


total_diff = []
for i in range(sims):
    print(i)
    refresh_BA()
    facebook.initialize_states()
    BA.initialize_states()

    # run simulation
    for j in range(time_steps):
        facebook.make_timestep()
        BA.make_timestep()

    # normalize number of infected nodes
    facebook_percent = [i / len(facebook.G.nodes)
                        for i in facebook.infected_at_t]
    BA_percent = [i / len(BA.G.nodes) for i in BA.infected_at_t]

    diffs = [np.abs(fb - ba) for fb, ba in zip(facebook_percent, BA_percent)]
    total_diff.append(np.sum(diffs))


with open('../Data/total_difference_save.txt', 'w') as f:
    for diff in total_diff:
        f.write(str(diff) + "\n")

plt.figure()
plt.title("Distribution of total differences of infection curves (FB vs BA)")
plt.hist(total_diff, density=True, bins=50)
plt.xlabel("Total difference (FB vs BA)")
plt.ylabel("Frequency")
plt.show()
plt.savefig("../Plots/total_difference_distribution.png")


# # plotting spread on both networks
# plt.figure(figsize=(10, 10))
# plt.plot(list(range(facebook.time_steps + 1)), facebook_percent,
#          label='Facebook')
# plt.plot(list(range(facebook.time_steps + 1)), BA_percent, label='BA')
# plt.xlabel("Timestep t")
# plt.ylabel("Amount infected nodes")
# plt.title("Amount of infected nodes at timestep t")
# plt.legend()
# plt.savefig("naive_facebookvsBA.png")
