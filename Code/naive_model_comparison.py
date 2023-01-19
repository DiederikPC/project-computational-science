import matplotlib.pyplot as plt
import numpy as np
from SocialGraph import SocialGraph

sims, i, i_init, time_steps = 40, 0.01, 0.1, 50

# open the facebook and barabasi-albert networks
facebook = SocialGraph("facebook_combined.txt", i, i_init, time_steps)
BA = SocialGraph("barabasi_albert.txt", i, i_init, time_steps)

surface = []
for _ in range(sims):
    facebook.initialize_states()
    BA.initialize_states()

    # run simulation
    for _ in range(time_steps):
        facebook.make_timestep()
        BA.make_timestep()

    # normalize number of infected nodes
    facebook_percent = [i / len(facebook.G.nodes) for i in facebook.infected_at_t]
    BA_percent = [i / len(BA.G.nodes) for i in BA.infected_at_t]

    diffs = [np.abs(fb - ba) for fb, ba in zip(facebook_percent, BA_percent)]
    surface.append(np.sum(diffs))


plt.figure()
plt.hist(surface, density=True)
plt.show()

# # plotting spread on both networks
# plt.figure(figsize=(10, 10))
# plt.plot(list(range(facebook.time_steps + 1)), facebook_percent, label='Facebook')
# plt.plot(list(range(facebook.time_steps + 1)), BA_percent, label='BA')
# plt.xlabel("Timestep t")
# plt.ylabel("Amount infected nodes")
# plt.title("Amount of infected nodes at timestep t")
# plt.legend()
# plt.savefig("naive_facebookvsBA.png")
#
