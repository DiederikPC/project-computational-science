import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

graph = nx.barabasi_albert_graph(4039, 20)
with open('barabasi_albert.txt', 'w') as f:
    for edge in graph.edges():
        f.write(str(edge[0]) + " " + str(edge[1]) + "\n")
