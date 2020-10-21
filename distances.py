import Hofstad_model as hm
import visualisation as vis
import networkx as nx
import numpy as np

def distance_functions_example_using_hofstad(num_pairs, delta=0, m=3, num_iterations=40):
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
            nx.all_pairs_shortest_path_length()
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


distance_functions_example_using_hofstad(num_pairs=5)
