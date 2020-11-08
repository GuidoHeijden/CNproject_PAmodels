import Hofstad_model as hm
import visualisation as vis
import networkx as nx
import numpy as np
from Alves_RIbeiro_Sanchis_edge_vertex import PA_model2
from Alves_Ribeiro_Sanchis_model import model_edgestepfunc, edgeStepFun1, edgeStepFun2, edgeStepFun3
import matplotlib.pyplot as plt
from random import sample
from collections import Counter


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
    This function returns the average distance based on a dictionary containing all distances
    between two vertices in a graph.

    :param dists: A dictionary of distances
    :return:      The average distance
    '''
    return sum(dists.values()) / len(dists)


def get_typical_distances(dists, num_dists):
    '''
    This function simulates the typical distance based on a dictionary containing all distances
    between two vertices in a graph, by selecting num_dists from that dictionary and returning those.

    :param dists:     A dictionary of distances
    :param num_dists: A dictionary of distances
    :return:          The average distance between two vertices in G
    '''

    if len(dists) <= 0:
        raise Exception("There should be at least one distance in the list of distance!")
    elif len(dists) < num_dists:
        raise Exception("There should be more distances than the number of distances asked!")

    return sample(list(dists.values()), num_dists)


def plot_diameter(model, m, num_iterations, num_experiments, p=0, e_fun=None, delta=0):
    '''
    This function plots the average diameter over time of num_experiments experiments, where
    the diameter of each experiment is plotted in the background as well. The function works
    for Hofstad model B (uses delta as affine parameter), the PA model with edge steps
    (uses probability p), and the PA model with edge-step function (uses function e_fun).

    :param model:           String that indicates which model to use, see below for the options
    :param m:               Edges to create between existing vertices and the new vertex at a timestep
    :param num_iterations:  At what t to stop the model to stop the simulation
    :param num_experiments: How many graphs to simulate to calculate the diameter over time
    :param p:               The probability of a vertex step for the PA model with edge steps
    :param e_fun:           The edge-step function for the PA model with edge-step function
    :param delta:           The affine parameter for Hofstad model B
    :return:
    '''

    # Model options:
    if model not in ["HofstadB", "EdgeStep", "EdgeStepFun"]:
        raise Exception("Use a valid model!")

    diameter_over_time = []

    for i in range(num_experiments):
        print("Current experiment:", i)  # Keep track of which experiment is running

        # Each model starts in the same way using the initial graph of two vertices
        # with 2m edges between them.
        diameter_over_time.append([])
        G = hm.hofstad_PA_start_b(m)
        diameter_over_time[i].append(get_diameter(G))

        # At each timestep, for each experiment, the diameter is calculated and stored
        # in the list of lists diameter_over_time. i is the current experiment
        for t_step in range(3, num_iterations + 1):
            if model == "HofstadB":
                G = hm.hofstad_PA_b(G, delta=delta, m=m, t=t_step-1, t_stop=t_step, verbose=0)
            elif model == "EdgeStep":
                G = PA_model2(G, m, p, t=t_step - 1, t_stop=t_step, verbose=0)
            elif model == "EdgeStepFun":
                G = model_edgestepfunc(G, m, edgestepfun=e_fun, t=t_step - 1, t_stop=t_step, verbose=0)
            diameter_over_time[i].append(get_diameter(G))

    # Visualize the last experiment/graph
    vis.display_graph(G, save_file='')

    fig, ax = plt.subplots()

    x = range(2, num_iterations + 1)
    for i in range(num_experiments):
        ax.plot(x, diameter_over_time[i], color='blue', alpha=0.2)

    diameter_average = []
    for i in range(num_iterations - 1):
        diameter_average.append(sum([diam[i] for diam in diameter_over_time]) / (num_experiments - 1))

    ax.plot(x, diameter_average, color='red', alpha=1)  # The average diameter will be plotted in red
    ax.set_xlabel('timestep')
    ax.set_ylabel('diameter')
    if model == "HofstadB":
        fig.suptitle('Diameter over time PA model with delta=' + str(delta), fontsize=12)
    elif model == "EdgeStep":
        fig.suptitle('Diameter over time PA model using Edge Step with p = '+str(p), fontsize=12)
    elif model == "EdgeStepFun":
        if e_fun == edgeStepFun1:
            fig.suptitle('Diameter over time PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
        elif e_fun == edgeStepFun2:
            fig.suptitle('Diameter over time PA model using Edge Function f(t)=1 / log_{base=2}(t)^2', fontsize=12)
        elif e_fun == edgeStepFun3:
            fig.suptitle('Diameter over time PA model using Edge Function f(t)=1 / log_{base=2}(t)', fontsize=12)

    plt.show()
    return


def histogram_typical_average_distance(model, m, at_which_t, frac_dists, p=0, e_fun=None, delta=0):
    '''
    This function plots a histogram of the typical distances for a model at predefined values of t.
    The function works for Hofstad model B (uses delta as affine parameter), the PA model with
    edge steps (uses probability p), and the PA model with edge-step function (uses function e_fun).

    :param model:      String that indicates which model to use, see below for the options
    :param m:          Edges to create between existing vertices and the new vertex at a timestep
    :param at_which_t: At which values of t the histogram should be plotted
    :param frac_dists: The fraction of distances that is used to simulate the typical distances
    :param p:          The probability of a vertex step for the PA model with edge steps
    :param e_fun:      The edge-step function for the PA model with edge-step function
    :param delta:      The affine parameter for Hofstad model B
    :return:
    '''

    # Model options:
    if model not in ["HofstadB", "EdgeStep", "EdgeStepFun"]:
        raise Exception("Use a valid model!")

    for t in at_which_t:
        if t < 2:
            raise Exception("Use valid values for t to plot the histograms: t > 2")

    average_distance_at_t = []
    typical_distance_at_t = []

    # Each model starts in the same way using the initial graph of two vertices
    # with 2m edges between them.
    G = hm.hofstad_PA_start_b(m)
    if 2 in at_which_t:
        dists = get_all_distances(G)
        average_distance_at_t.append(get_average_distance(dists=dists))
        num_dists = int(len(dists) * frac_dists)
        typical_distance_at_t.append(get_typical_distances(dists=dists, num_dists=num_dists))

    # At each timestep in at_which_t the average distance and typical distance
    # is calculated and stored the corresponding list
    for t_step in range(3, max(at_which_t) + 1):
        if model == "HofstadB":
            G = hm.hofstad_PA_b(G, delta=delta, m=m, t=t_step-1, t_stop=t_step, verbose=0)
        elif model == "EdgeStep":
            G = PA_model2(G, m, p, t=t_step - 1, t_stop=t_step, verbose=0)
        elif model == "EdgeStepFun":
            G = model_edgestepfunc(G, m, edgestepfun=e_fun, t=t_step - 1, t_stop=t_step, verbose=0)
        if t_step in at_which_t:
            dists = get_all_distances(G)
            average_distance_at_t.append(get_average_distance(dists=dists))
            num_dists = int(len(dists) * frac_dists)
            typical_distance_at_t.append(get_typical_distances(dists=dists, num_dists=num_dists))

    # Visualize the final graph
    vis.display_graph(G, save_file='')

    # Plot each of the histograms
    for i, t in enumerate(at_which_t):
        fig = plt.figure(i+1)

        print("Typical distances at time t="+str(t)+" :", typical_distance_at_t[i])
        plt.hist(typical_distance_at_t[i], max(typical_distance_at_t[i])-min(typical_distance_at_t[i])+1)
        plt.xlabel('distance')
        plt.ylabel('occurrence')
        if model == "HofstadB":
            fig.suptitle('Distances at t='+str(t)+' for PA model with delta=' + str(delta), fontsize=12)
        elif model == "EdgeStep":
            fig.suptitle('Distances at t='+str(t)+' for PA model using Edge Step with p = ' + str(p), fontsize=12)
        elif model == "EdgeStepFun":
            if e_fun == edgeStepFun1:
                fig.suptitle('Distances at t='+str(t)+' for PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
            elif e_fun == edgeStepFun2:
                fig.suptitle('Distances at t='+str(t)+' for PA model using Edge Function f(t)=1 / log_{base=2}(t)^2', fontsize=12)
            elif e_fun == edgeStepFun3:
                fig.suptitle('Distances at t='+str(t)+' for PA model using Edge Function f(t)=1 / log_{base=2}(t)', fontsize=12)

    plt.show()
    return


def plot_typical_average_distance(model, m, at_which_t, frac_dists, p=0, e_fun=None, delta=0):
    '''
    This function plots a histogram of the typical distances for a model at predefined values of t.
    The function works for Hofstad model B (uses delta as affine parameter), the PA model with
    edge steps (uses probability p), and the PA model with edge-step function (uses function e_fun).

    :param model:      String that indicates which model to use, see below for the options
    :param m:          Edges to create between existing vertices and the new vertex at a timestep
    :param at_which_t: At which values of t the histogram should be plotted
    :param frac_dists: The fraction of distances that is used to simulate the typical distances
    :param p:          The probability of a vertex step for the PA model with edge steps
    :param e_fun:      The edge-step function for the PA model with edge-step function
    :param delta:      The affine parameter for Hofstad model B
    :return:
    '''

    # Model options:
    if model not in ["HofstadB", "EdgeStep", "EdgeStepFun"]:
        raise Exception("Use a valid model!")

    for t in at_which_t:
        if t < 2:
            raise Exception("Use valid values for t to plot the histograms: t > 2")

    average_distance_at_t = []
    typical_distance_at_t = []
    average_distances = []

    # Each model starts in the same way using the initial graph of two vertices
    # with 2m edges between them.
    G = hm.hofstad_PA_start_b(m)
    # average_distances.append(get_average_distance(dists=dists))
    if 2 in at_which_t:
        dists = get_all_distances(G)
        average_distance_at_t.append(get_average_distance(dists=dists))
        num_dists = int(len(dists) * frac_dists)
        typical_distance_at_t.append(get_typical_distances(dists=dists, num_dists=num_dists))


    # At each timestep in at_which_t the average distance and typical distance
    # is calculated and stored the corresponding list
    for t_step in range(3, max(at_which_t) + 1):
        print("Current timestep:", t_step)
        if model == "HofstadB":
            G = hm.hofstad_PA_b(G, delta=delta, m=m, t=t_step-1, t_stop=t_step, verbose=0)
        elif model == "EdgeStep":
            G = PA_model2(G, m, p, t=t_step - 1, t_stop=t_step, verbose=0)
        elif model == "EdgeStepFun":
            G = model_edgestepfunc(G, m, edgestepfun=e_fun, t=t_step - 1, t_stop=t_step, verbose=0)
        # average_distances.append(get_average_distance(dists=dists))
        if t_step in at_which_t:
            dists = get_all_distances(G)
            average_distance_at_t.append(get_average_distance(dists=dists))
            num_dists = int(len(dists) * frac_dists)
            typical_distance_at_t.append(get_typical_distances(dists=dists, num_dists=num_dists))

    # Visualize the final graph
    vis.display_graph(G, save_file='')

    # Plot each of the histograms
    fig = plt.figure()

    for i, t in enumerate(at_which_t):
        dist_counter = Counter(typical_distance_at_t[i])
        maximum = max(dist_counter.values())
        for distance, count in dist_counter.items():
            plt.scatter(t, distance, color='b', alpha=count/maximum)
    plt.scatter(at_which_t, average_distance_at_t, color='r', alpha=1)

    # x = range(2, max(at_which_t) + 1)
    # plt.plot(x, average_distances, color='r', alpha=1)

    plt.xlabel('timestep')
    plt.ylabel('distance')
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    if model == "HofstadB":
        fig.suptitle('Distances for PA model with delta=' + str(delta), fontsize=12)
    elif model == "EdgeStep":
        fig.suptitle('Distances for PA model using Edge Step with p = ' + str(p), fontsize=12)
    elif model == "EdgeStepFun":
        if e_fun == edgeStepFun1:
            fig.suptitle('Distances for PA model using Edge Function f(t)=1 / t^1.01', fontsize=12)
        elif e_fun == edgeStepFun2:
            fig.suptitle('Distances for PA model using Edge Function f(t)=1 / log_{base=2}(t)^2', fontsize=12)
        elif e_fun == edgeStepFun3:
            fig.suptitle('Distances for PA model using Edge Function f(t)=1 / log_{base=2}(t)', fontsize=12)

    plt.show()
    return


# plot_diameter(model="HofstadB", m=1, num_iterations=100, num_experiments=50, delta=0)

# histogram_typical_average_distance(model="EdgeStepFun", m=1, at_which_t=[10, 100, 500, 1000, 1500, 2000],
#                               frac_dists=0.5, e_fun=edgeStepFun1)

plot_typical_average_distance(model="EdgeStepFun", m=1, at_which_t=list(range(500, 10000, 500)),
                              frac_dists=0.5, e_fun=edgeStepFun3)
