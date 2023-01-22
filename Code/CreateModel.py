import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class CreateModel:
    def create_BA():
        graph = nx.barabasi_albert_graph(4039, 20)
