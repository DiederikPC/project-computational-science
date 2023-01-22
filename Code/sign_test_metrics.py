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
    G = None

    def initialize_states(self):
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

    def __init__(self, edgelist, i, i_init, time_steps):
        self.G = nx.read_edgelist("../Data/" + edgelist, delimiter=' ')
        self.i = i
        self.i_init = i_init
        self.time_steps = time_steps

        self.initialize_states()


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
        plt.savefig("../Plots/" + title + ".png")
        if show:
            plt.show()

    def show_infected_plot(self, title):
        """
            Plot the amount of infected nodes in a graph.
        """
        # normalize number of infected nodes
        infected_at_t_percent = [i / len(self.G.nodes) for i in self.infected_at_t]
        plt.figure(figsize=(10, 10))
        plt.plot(list(range(self.time_steps + 1)), infected_at_t_percent)
        plt.xlabel("Timestep t")
        plt.ylabel("Amount infected nodes")
        plt.title("Amount of infected nodes at timestep t")
        plt.savefig("../Plots/" + title)

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


# SIGNIFICANCE TEST OF DIFFERENCE IN DIFFERENT METRICS' DISTRIBUTION BETWEEN FB AND BA NETWORK
import math
from scipy.stats import ks_2samp

#0. GENERAL PARAMETERS
sims, i, i_init, time_steps, network_iters = 500, 0.01, 0.001, 30, 50

# 1. OBTAIN METRIC DISTRIBUTION FROM BA NETWORK 
reach_list_BA = []

# FOR THE MOMENT I DEFINE SPEED AS TIME STEPS UNTIL 80% POPULATION INFECTED
speed_list_BA = []
raw_deg_list_BA = []

for iter in range(network_iters):
    BA = SocialGraph(r"barabasi_albert.txt", i, i_init, time_steps)
    speed_add = True
    for u in range(time_steps):
        BA.make_timestep()
        if (BA.inf_count/len(BA.G.nodes()) >= 0.8) and (speed_add):
            speed_list_BA.append(u)          
            speed_add = False
    
    raw_deg_list_BA.append(BA.inf_degree_avg)
    reach_list_BA.append(BA.inf_count)

BA_list_per_step = [[] for i in range(time_steps)]
for i in range(time_steps):
    for u in range(network_iters):
        if math.isnan(raw_deg_list_BA[u][i]) == False: 
            BA_list_per_step[i].append(raw_deg_list_BA[u][i])

deg_list_BA = [np.mean(i) for i in BA_list_per_step]

#2. OBTAIN METRIC DISTRIBUTION FROM FB NETWORK
reach_list_FB = []
speed_list_FB = []
raw_deg_list_FB = []

for iter in range(network_iters):
    FB = SocialGraph(r"facebook_combined.txt", i, i_init, time_steps)
    speed_add = True
    for u in range(time_steps):
        FB.make_timestep()
        if (FB.inf_count/len(FB.G.nodes()) >= 0.8) and (speed_add):
            speed_list_FB.append(u)          
            speed_add = False
    
    raw_deg_list_FB.append(FB.inf_degree_avg)
    reach_list_FB.append(FB.inf_count)


# to be computed 
FB_list_per_step = [[] for i in range(time_steps)]
for i in range(time_steps):
    for u in range(network_iters):
        if math.isnan(raw_deg_list_FB[u][i]) == False:
            FB_list_per_step[i].append(raw_deg_list_FB[u][i])

deg_list_FB = [np.mean(i) for i in FB_list_per_step]

#3. COMPARE METRIC DISTRIBUTIONS

# KOLMOGOROV-SMIRNOV TO TEST DIFFERENCE BETWEEN REACH AND SPEED DISTRIBUTIONS
ks_2samp(reach_list_BA,reach_list_FB)
ks_2samp(speed_list_BA,speed_list_FB)


# PLOT COMPARING REACH (SAME SHOULD BE DONE FOR SPEED)
plt.hist(reach_list_BA,bins = 30,label = 'BA')
plt.hist(reach_list_FB,color = 'red',bins = 30,label = 'FB')
plt.legend()
plt.show()

# PLOT COMPARING SPEED 
plt.hist(speed_list_BA,bins = 10,label = 'BA')
plt.hist(speed_list_FB, bins = 10, color = 'red',label = 'FB')
plt.legend()
plt.show()

# PLOT COMPARING DEGREE INFECTED NODES PER TIMESETP 
plt.plot(range(time_steps),deg_list_BA,color = 'red',label = 'BA')
plt.plot(range(time_steps),deg_list_FB,color = 'blue',label = 'FB')
plt.legend()
plt.show()



