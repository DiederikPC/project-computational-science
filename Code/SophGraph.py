from SocialGraph import SocialGraph


class SophGraph(SocialGraph):

    def __init__(self, edgelist, i, i_init, time_steps, decay_rate):
        self.decay_rate = decay_rate
        super().__init__(edgelist, i, i_init, time_steps)

        self.t_infected = {k: 0 for k in self.node_states
                           if self.node_states[k] == 1}

    def make_timestep(self):
        super.make_timestep()
        self.t_infected = {k: v+1 for k, v in self.node_states.items()}
        self.t_infected = {k: 0 for k, v in self.node_states.items() if v == 1
                           and k not in self.t_infected.keys()}
