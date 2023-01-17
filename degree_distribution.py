import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_edgelist('facebook_combined.txt', delimiter=' ')
degrees = sorted([degree for node, degree in G.degree()])


fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Degree distribution (linear vs log)')
ax1.hist(degrees, bins=40, density=True)
ax2.hist(degrees, bins=40, density=True, log=True)
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.show()
