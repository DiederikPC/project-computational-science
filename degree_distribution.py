import matplotlib.pyplot as plt
import networkx as nx

facebook = nx.read_edgelist('facebook_combined.txt', delimiter=' ')
facebook_degrees = sorted([degree for node, degree in facebook.degree()])

ba = nx.read_edgelist('barabasi_albert.txt', delimiter=' ')
ba_degrees = sorted([degree for node, degree in ba.degree()])


fig, axs = plt.subplots(2, 2)
axs[0, 0].hist(facebook_degrees, density=True, bins=50)
axs[0, 0].set_title('Facebook degree distribution')
axs[0, 1].hist(facebook_degrees, density=True, log=True, bins=50)
axs[0, 1].set_title('Facebook log degree distribution')
axs[1, 0].hist(ba_degrees, density=True, bins=50)
axs[1, 0].set_title('BA degree distribution')
axs[1, 1].hist(ba_degrees, density=True, log=True, bins=50)
axs[1, 1].set_title('BA log degree distribution')
plt.show()
