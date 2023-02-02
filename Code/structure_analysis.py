import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def get_shortest_path_average(FB, BA, BA_averaging=False):
    """
    Calculates the average shortest path of the emperical Facebook network
    and a Barabasi-Albert network. Has the option to average over
    30 BA's.
    """

    # FB shortest path
    FB_shortest = nx.average_shortest_path_length(FB)

    # calculate average shortest path of 30 BA's if averaging is True
    if not BA_averaging:
        BA_shortest = nx.average_shortest_path_length(BA)
        return FB_shortest, BA_shortest
    else:
        BA_shortest_paths = []
        for _ in range(30):
            BA = nx.barabasi_albert_graph(4039, 22)
            BA_shortest_paths.append(nx.average_shortest_path_length(BA))
        return (FB_shortest, np.mean(BA_shortest_paths),
                np.std(BA_shortest_paths))


def get_diameter(FB, BA, BA_averaging=False):
    """
    Calculates the diameter of the emperical Facebook network
    and a Barabasi-Albert network. Has the option to average over
    30 BA's.
    """

    # FB diameter
    FB_diameter = nx.diameter(FB)

    # calculate average diameter of 30 BA's if averaging is True
    if not BA_averaging:
        BA_diameter = nx.diameter(BA)
        return FB_diameter, BA_diameter
    else:
        BA_diameters = []
        for _ in range(30):
            BA = nx.barabasi_albert_graph(4039, 22)
            BA_diameters.append(nx.diameter(BA))
        return FB_diameter, np.mean(BA_diameters), np.std(BA_diameters)


def get_clustering_coeff(FB, BA, BA_averaging=False):
    """
    Calculates the clustering coefficient of the emperical Facebook network
    and a Barabasi-Albert network. Has the option to average over
    30 BA's.
    """

    # FB clustering coefficient
    FB_clust_coeff = nx.average_clustering(FB)

    # calculate clustering coefficient of 30 BA's if averaging is True
    if not BA_averaging:
        BA_clust_coeff = nx.average_clustering(BA)
        return FB_clust_coeff, BA_clust_coeff
    else:
        BA_clust_coeffs = []
        for _ in range(30):
            BA = nx.barabasi_albert_graph(4039, 22)
            BA_clust_coeffs.append(nx.average_clustering(BA))
        return (FB_clust_coeff, np.mean(BA_clust_coeffs),
                np.std(BA_clust_coeffs))


def get_degree_dist(FB, BA, BA_averaging=False):
    """
    Calculates the degree distribution of the emperical Facebook network
    and a Barabasi-Albert network. Has the option to average over
    30 BA's.

    """

    # create figure for multiple subplots
    fig, axs = plt.subplots(3, 2)

    # create FB subplots
    FB_degree_dist = sorted([degree for _, degree in FB.degree()],
                            reverse=True)
    axs[0, 0].plot(FB_degree_dist, marker="o")
    axs[0, 1].hist(FB_degree_dist, log=True, bins=50)

    # create BA subplots, take average degrees from 30 BA's if 
    # averaging is True
    if not BA_averaging:
        BA_degree_dist = sorted([degree for _, degree in BA.degree()],
                                reverse=True)
        axs[1, 0].plot(BA_degree_dist, "tab:orange", marker="o")
        axs[1, 1].hist(BA_degree_dist, log=True, bins=50, color="tab:orange")
    else:
        BA_degree_dists = []
        for _ in range(30):
            BA = nx.barabasi_albert_graph(4039, 22)
            BA_degree_dists.append(sorted([degree for _,
                                           degree in BA.degree()],
                                          reverse=True))

        BA_avg_degree_dist = [np.mean([n[i] for n in BA_degree_dists])
                              for i in range(len(BA_degree_dists[0]))]
        axs[1, 0].plot(BA_avg_degree_dist, "tab:orange", marker="o")
        axs[1, 1].hist(BA_avg_degree_dist, log=True, bins=50,
                       color="tab:orange")

    # set titles and axis labels for FB and BA subplots
    axs[0, 0].set_title('FB degree-rank plot')
    axs[0, 0].set_ylabel("Degree")
    axs[0, 0].set_xlabel("Rank")

    axs[0, 1].set_title('FB degree histogram')
    axs[0, 1].set_ylabel("# of nodes")
    axs[0, 1].set_xlabel("Degree")

    axs[1, 0].set_title('BA degree-rank plot')
    axs[1, 0].set_ylabel("Degree")
    axs[1, 0].set_xlabel("Rank")

    axs[1, 1].set_title('BA degree histogram')
    axs[1, 1].set_ylabel("# of nodes")
    axs[1, 1].set_xlabel("Degree")

    # create combined FB/BA subplot
    axs[2, 0].plot(FB_degree_dist)
    axs[2, 0].plot(BA_avg_degree_dist, "tab:orange")

    axs[2, 1].hist(FB_degree_dist, log=True, bins=50)
    axs[2, 1].hist(BA_avg_degree_dist, log=True, bins=50, color='tab:orange')

    axs[2, 0].set_title('FB/BA degree-rank plot')
    axs[2, 0].set_ylabel("Degree")
    axs[2, 0].set_xlabel("Rank")

    axs[2, 1].set_title('FB/BA degree histogram')
    axs[2, 1].set_ylabel("# of nodes")
    axs[2, 1].set_xlabel("Degree")

    # show figure with subplots
    fig.tight_layout()
    plt.show()

    return


def get_centralities(FB, BA, visualize=False):
    """
    Calculates the degree centrality, betweenness centrality and
    closeness centrality of the emperical Facebook network
    and a Barabasi-Albert network.
    Also creates a score with the 3 centralities combined.
    """

    # # DEGREE #
    # # calculate degree centrality for each node
    FB_degree = nx.degree_centrality(FB)
    FB_degree = sorted(FB_degree.items(), key=lambda x: x[1], reverse=True)
    FB_degree_scores = [score for _, score in FB_degree]

    BA_degree = nx.degree_centrality(BA)
    BA_degree = sorted(BA_degree.items(), key=lambda x: x[1], reverse=True)
    BA_degree_scores = [score for _, score in BA_degree]

    # visualize degree centrality distribution
    if visualize:
        fig, axs = plt.subplots(2, 2)

        axs[0, 0].hist(FB_degree_scores, log=True, bins=50)
        axs[0, 1].plot(FB_degree_scores, marker="o")
        axs[1, 0].hist(BA_degree_scores, log=True, bins=50, color="tab:orange")
        axs[1, 1].plot(BA_degree_scores, "tab:orange", marker="o")

        fig.tight_layout()
        plt.show()

    # show degree centrality values
    FB_mean = np.mean(FB_degree_scores)
    FB_std = np.std(FB_degree_scores)
    BA_mean = np.mean(BA_degree_scores)
    BA_std = np.std(BA_degree_scores)
    print(f'FB degree centrality mean: {np.mean(FB_mean)}, std: {FB_std}')
    print(f'BA degree centrality mean: {np.mean(BA_mean)}, std: {BA_std}')


    # # BETWEENNESS #
    # # calculate betweenness centrality for each node
    FB_betweenness = nx.betweenness_centrality(FB)
    FB_betweenness = sorted(FB_betweenness.items(), key=lambda x: x[1],
                            reverse=True)
    FB_betweenness_scores = [score for _, score in FB_betweenness]

    BA_betweenness = nx.betweenness_centrality(BA)
    BA_betweenness = sorted(BA_betweenness.items(), key=lambda x: x[1],
                            reverse=True)
    BA_betweenness_scores = [score for _, score in BA_betweenness]

    # visualize degree centrality distribution
    if visualize:
        fig, axs = plt.subplots(2, 2)

        axs[0, 0].hist(FB_betweenness_scores, log=True, bins=50)
        axs[0, 1].plot(FB_betweenness_scores, marker="o")
        axs[1, 0].hist(BA_betweenness_scores, log=True, bins=50, color="tab:orange")
        axs[1, 1].plot(BA_betweenness_scores, "tab:orange", marker="o")

        fig.tight_layout()
        plt.show()

    # show betweenness centrality values
    FB_mean = np.mean(FB_betweenness_scores)
    FB_std = np.std(FB_betweenness_scores)
    BA_mean = np.mean(BA_betweenness_scores)
    BA_std = np.std(BA_betweenness_scores)
    print(f'FB betweenness centrality mean: {np.mean(FB_mean)}, std: {FB_std}')
    print(f'BA betweenness centrality mean: {np.mean(BA_mean)}, std: {BA_std}')


    # # CLOSENESS #
    # # calculate closensee centrality for each node
    FB_closeness = nx.closeness_centrality(FB)
    FB_closeness = sorted(FB_closeness.items(), key=lambda x: x[1],
                          reverse=True)
    FB_closeness_scores = [score for _, score in FB_closeness]

    BA_closeness = nx.closeness_centrality(BA)
    BA_closeness = sorted(BA_closeness.items(), key=lambda x: x[1],
                          reverse=True)
    BA_closeness_scores = [score for _, score in BA_closeness]

    # visualize degree centrality distribution
    if visualize:
        fig, axs = plt.subplots(2, 2)

        axs[0, 0].hist(FB_closeness_scores, log=True, bins=50)
        axs[0, 1].plot(FB_closeness_scores, marker="o")
        axs[1, 0].hist(BA_closeness_scores, log=True, bins=50, color="tab:orange")
        axs[1, 1].plot(BA_closeness_scores, "tab:orange", marker="o")

        fig.tight_layout()
        plt.show()

    # show closeness centrality values
    FB_mean = np.mean(FB_closeness_scores)
    FB_std = np.std(FB_closeness_scores)
    BA_mean = np.mean(BA_closeness_scores)
    BA_std = np.std(BA_closeness_scores)
    print(f'FB closeness centrality mean: {np.mean(FB_mean)}, std: {FB_std}')
    print(f'BA closeness centrality mean: {np.mean(BA_mean)}, std: {BA_std}')


    # INFLUENTIAL SCORES #
    # calculate individual node influence scores (the lower the better)

    # FB centralities
    FB_centralities = [FB_degree, FB_betweenness, FB_closeness]
    FB_centrality_scores = {str(node): 0 for node in FB.nodes()}

    for centrality in FB_centralities:
        for i, (node, _) in enumerate(centrality):
            FB_centrality_scores[str(node)] += i

    FB_centrality_scores = sorted(FB_centrality_scores.items(),
                                  key=lambda x: x[1])
    FB_centrality_nodes = [node for (node, _) in FB_centrality_scores]
    FB_centrality_scores = [score for (_, score) in FB_centrality_scores]

    # BA centralities
    BA_centralities = [BA_degree, BA_betweenness, BA_closeness]
    BA_centrality_scores = {str(node): 0 for node in BA.nodes()}

    for centrality in BA_centralities:
        for i, (node, _) in enumerate(centrality):
            BA_centrality_scores[str(node)] += i

    BA_centrality_scores = sorted(BA_centrality_scores.items(),
                                  key=lambda x: x[1])
    BA_centrality_nodes = [node for (node, _) in BA_centrality_scores]
    BA_centrality_scores = [score for (_, score) in BA_centrality_scores]

    # visualize centrality scores distribution
    if visualize:
        fig, axs = plt.subplots(2, 2)

        axs[0, 0].hist(FB_centrality_scores, log=False, bins=50)
        axs[0, 1].plot(FB_centrality_scores, marker="o")
        axs[1, 0].hist(BA_centrality_scores, log=False, bins=50, color="tab:orange")
        axs[1, 1].plot(BA_centrality_scores, "tab:orange", marker="o")

        fig.tight_layout()
        plt.show()

    return FB_centrality_nodes, BA_centrality_nodes


if __name__ == '__main__':
    FB = nx.read_edgelist("../Data/facebook_combined.txt", delimiter=' ')
    BA = nx.barabasi_albert_graph(4039, 22)

    # average shortest path
    print(get_shortest_path_average(FB, BA, BA_averaging=True))

    # diameter
    print(get_diameter(FB, BA, BA_averaging=True))

    # clustering coefficient
    print(get_clustering_coeff(FB, BA, BA_averaging=False))

    # degree distribution
    get_degree_dist(FB, BA, BA_averaging=True)

    # centrality measures
    print(get_centralities(FB, BA, visualize=True))
