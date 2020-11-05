import Hofstad_model as hm
import visualisation as vis
import networkx as nx
import numpy as np
from Alves_RIbeiro_Sanchis_edge_vertex import PA_model2
from Alves_Ribeiro_Sanchis_model import model_edgestepfunc, edgeStepFun1
import matplotlib.pyplot as plt
import seaborn as sns


def distance_functions_example_using_hofstad(num_pairs, delta=0, m=1, num_iterations=10000):
    '''
    This function generates a Hofstad model-a graph and then calculates:
    - The diameter of the graph
    - The average distance between vertices in the graph
    - The typical distance for num_pairs pairs

    :param num_pairs:       The num_pairs used to calculate the average typical distance
    :param delta:           An affine attachment rule parameter
    :param m:               Number of edges that are attached to a new vertex
    :param num_iterations:  The timestep after which to stop the simulation
    :return:                Nothing
    '''
    verbosity = 0

    G = hm.hofstad_PA_start(m)
    G = hm.hofstad_PA(G, delta, m, t=1, t_stop=num_iterations, verbose=verbosity)

    vis.display_graph(G, save_file="")

    all_distances = get_all_distances(G)
    print(get_diameter(G))
    print(all_distances)
    print(get_average_distance(all_distances))
    print(get_typical_distances(num_pairs, all_distances, G))

def get_diameter(G):
    '''
    This function returns the diameter of graph G using the NetworkX library.

    :param G: A graph G
    :return:  The diameter of graph G
    '''
    return nx.diameter(G)


def get_all_distances(G):
    '''
    This function returns the distances between each pair of vertices in graph G
    and returns these distances as a dictionary

    :param G: A graph G
    :return:  Dictionary containing distances --- { (vertex_1, vertex_2) : distance }
    '''
    distances = {}
    for v_1 in G.nodes():
        for v_2 in G.nodes():
            if v_2 <= v_1:
                continue
            distances[(v_1, v_2)] = nx.shortest_path_length(G, source=v_1, target=v_2)
    return distances


def get_average_distance(dists):
    '''
    This function returns the diameter of graph G using the NetworkX library.

    :param dists: A dictionary of distances
    :return:      The average distance between two vertices in G
    '''
    return sum(dists.values()) / len(dists)


def get_typical_distances(num_pairs, dists, G):
    typical_distances = []

    num_vertices = len(G.nodes())
    if num_vertices <= 1:
        raise Exception("There should be more than 1 vertex in a Graph to calculate the distances!")

    for i in range(num_pairs):
        v_1, v_2 = np.random.randint(1, num_vertices+1, 2)
        while v_1 == v_2:
            v_2 = np.random.randint(1, num_vertices, 1)
        typical_distances.append(nx.shortest_path_length(G, source=v_1, target=v_2))

    return typical_distances


# distance_functions_example_using_hofstad(num_pairs=5)

m = 1
delta = 0
num_iterations = 10000
num_pairs = 25
p = 2 - 3**0.5
e_fun = edgeStepFun1
experiments = 50
diameter_over_time = []
av_dist_over_time = []
typical_distance_over_time = []

for i in range(experiments):
    diameter_over_time.append([])
    av_dist_over_time.append([])
    typical_distance_over_time.append([])
    G = hm.hofstad_PA_start_b(m)
    diameter_over_time[i].append(get_diameter(G))
    av_dist_over_time[i].append(get_average_distance(get_all_distances(G)))
    #typical_distance_over_time[i].append(get_typical_distances(num_pairs, G))
    for t_step in range(3, num_iterations+1):
        # G = PA_model2(G, m, p, t=t_step-1, t_stop=t_step, verbose=0)
        # G = hm.hofstad_PA_b(G, delta=delta, m=m, t=t_step-1, t_stop=t_step, verbose=0)
        G = model_edgestepfunc(G, m, edgestepfun=e_fun, t=t_step - 1, t_stop=t_step, verbose=0)
        diameter_over_time[i].append(get_diameter(G))
        av_dist_over_time[i].append(get_all_distances(G))
        #typical_distance_over_time[i].append(get_typical_distances(num_pairs, dists=10, G))
    print("Hello there")
# fig, ax = plt.subplots()
#
# x = range(2, num_iterations+1)
# for i in range(experiments):
#     ax.plot(x, diameter_over_time[i], color='blue', alpha=0.2)
#
# diameter_average = []
# for i in range(num_iterations-1):
#     diameter_average.append(sum([diam[i] for diam in diameter_over_time]) / (experiments-1))
#
# ax.plot(x, diameter_average, color='red', alpha=1)
# # fig.suptitle('Diameter over time PA model using Edge Step with p = 2-sqrt(3)', fontsize=12)
# # fig.suptitle('Diameter over time PA model with delta=0', fontsize=12)
# fig.suptitle('Diameter over time PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
#
#
# plt.show()

fig, ax = plt.subplots()

ax.hist(av_dist_over_time, binwidth = 5, color = 'blue', edgecolor = 'black')
fig.suptitle('Average distance over time PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
plt.show()

# fig, ax = plt.subplots()
#
# x = range(2, num_iterations+1)
# for i in range(experiments):
#     ax.plot(x, typical_distance_over_time[i], color='blue', alpha=0.2)
#
# typical_distance_average = []
# for i in range(num_iterations-1):
#     typical_distance_average.append(sum([av[i] for av in typical_distance_over_time]) / (experiments-1))
#
# ax.plot(x, typical_distance_average, color='red', alpha=1)
# # fig.suptitle('Diameter over time PA model using Edge Step with p = 2-sqrt(3)', fontsize=12)
# # fig.suptitle('Diameter over time PA model with delta=0', fontsize=12)
# fig.suptitle('Typical distance over time PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
# plt.show()