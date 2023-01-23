import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from SocialGraph import SocialGraph
import math
from scipy.stats import ks_2samp

# SIGNIFICANCE TEST OF DIFFERENCE IN DIFFERENT METRICS' DISTRIBUTION BETWEEN FB AND BA NETWORK

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



