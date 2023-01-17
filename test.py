from SocialGraph import SocialGraph

if __name__ == "__main__":
    G = SocialGraph('facebook_combined.txt', 0.001, 0.001, 1000)

    # FbGraph.draw_graph("Before", True)

    for i in range(G.time_steps):
        print(f"Timestep {i}, infected nodes: {G.make_timestep()}")

    # FbGraph.draw_graph("After", True)
    G.show_infected_plot()
    