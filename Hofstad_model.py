import networkx as nx
import time
import numpy as np
import visualisation

def main():
    '''
    This function starts asking for input to the user in order to correctly run a
    simulation of one of the Preferential Attachment models described by Remco Hofstad.
    '''
    which_model    = str(input('Which Hofstad model do you want to use? (a | b)\n'))
    delta          = float(input('Enter the value of delta\n'))
    m              = int(input('Enter the value of m\n'))
    num_iterations = int(input('Enter the number of iterations, i.e. at what t to stop\n'))
    verbosity      = int(input("How verbose do you want the simulation to be? (0 | 1 | 2)\n"
                               "---- 0 : only show and save final graph\n"
                               "---- 1 : show probability distribution and selected vertices per iteration\n"
                               "---- 2 : show graph on each iteration (1.5 second breaks between iterations)\n"))

    # Throw exceptions for incorrect input
    if verbosity < 0 or verbosity > 2:
        raise Exception("Enter a correct value for verbosity!")
    if m < 0:
        raise Exception("m should be greater than zero!")
    if delta < -m:
        raise Exception("delta should be greater or equal to m!\ndelta: " + str(delta) + "\nm: " + str(m))
    if num_iterations < 2:
        raise Exception("There should be at least two iterations!")

    # Run the correct model
    if which_model == "a":
        G = hofstad_PA_start(m)
        G = hofstad_PA(G, delta, m, t=1, t_stop=num_iterations, verbose=verbosity)
    elif which_model == "b":
        G = hofstad_PA_start_b(m)
        G = hofstad_PA_b(G, delta, m, t=2, t_stop=num_iterations, verbose=verbosity)
    else:
        raise Exception("Enter a correct model version!")
    visualisation.display_graph(G)


def hofstad_PA_start(m=1):
    '''
    Create a Graph containing a single vertex with m self-loops. This is needed to prepare the graph
    for recursively simulating a Hofstad PA graph.

    :param m: Amount of self-loops on the initial vertex
    :return:  The Graph with the single vertex
    '''
    G = nx.MultiGraph()
    G.add_node(1)
    for i in range(m):
        G.add_edge(1, 1)
    return G


def hofstad_PA(G, delta, m, t, t_stop=10, verbose=True):
    '''
    Recursively simulate a Hofstad Preferential Attachment graph where at each timestep t, a single vertex is added
    with m edges. The vertex/vertices that these/this edge(s) attach to are defined by probability distribution P, which
    depends on delta and the degree of each vertex.
    The function will stop after t_stop iterations (this includes the initialization at t=1).

    :param G:       The Graph that is used for simulating Hofstad's model
    :param delta:   An affine attachment rule parameter
    :param m:       Number of edges that are attached to a new vertex
    :param t:       The current timestep of the simulation
    :param t_stop:  The timestep after which to stop the simulation
    :param verbose: Whether to print a verbose output of the simulation, including visualising graph G
    :return:
    '''
    for t in range(t, t_stop):
        ProbDists = []
        second_nodes = []
        for i in range(m):
            ProbDist = []
            for n in G.nodes():
                ProbDist.append((G.degree(n) + delta) / (t * (2 * m + delta) + (m + delta + 2 * i)))
            if i == 0:
                ProbDist.append( (m + delta) / (t*(2*m + delta) + (m + delta)) )
                G.add_node(t + 1)
            else:
                ProbDist.pop()
                ProbDist.append( (m + G.degree(n) + delta) / (t*(2*m + delta) + (m + delta + 2*i)) )
            second_node = np.random.choice(range(1, t+2), 1, ProbDist)[0]
            G.add_edge(t+1, second_node)
            ProbDists.append(ProbDist)
            second_nodes.append(second_node)

        if verbose >= 1:
            print("Iteration t =", t)
            print("Vertices and probability of attachment:")
            for i, P in enumerate(ProbDists):
                print(i, {n : p for n, p in zip(range(1, t + 2), P)})
                print("Sum of probability distribution = ", sum(P), "| selected vertex :", second_nodes[i])
            print("Randomly picked vertex/vertices for attachment:", second_nodes)
            print()
        if verbose >= 2:
            visualisation.display_graph(G, save_file="")
            time.sleep(1.5)
    return G


def hofstad_PA_start_b(m=1):
    '''
    Create a Graph containing a single vertex with no edges. This is needed to prepare the graph
    for recursively simulating a Hofstad PA graph version b.

    :param m: Used for consistency
    :return:  The Graph with the single vertex
    '''
    G = nx.MultiGraph()
    G.add_node(1)
    G.add_node(2)
    for i in range(m):
        G.add_edge(1, 2)
        G.add_edge(2, 1)
    return G

def hofstad_PA_b(G, delta, m, t, t_stop=10, verbose=True):
    '''
    Recursively simulate a Hofstad Preferential Attachment graph where at each timestep t, a single vertex is added
    with m edges. The vertex/vertices that these/this edge(s) attach to are defined by probability distribution P, which
    depends on delta and the degree of each vertex. Opposed to the other version of Hofstad's PA model, this version
    does not allow for self-loops.
    The function will stop after t_stop iterations (this includes the initialization at t=1).

    :param G:       The Graph that is used for simulating Hofstad's model
    :param delta:   An affine attachment rule parameter
    :param m:       Number of edges that are attached to a new vertex
    :param t:       The current timestep of the simulation
    :param t_stop:  The timestep after which to stop the simulation
    :param verbose: Whether to print a verbose output of the simulation, including visualising graph G
    :return:
    '''
    for t in range(t, t_stop):
        ProbDists = []
        second_nodes = []
        for i in range(m):
            ProbDist = []
            for n in G.nodes():
                ProbDist.append( (G.degree(n) + delta) / (t*(2*m + delta) + i) )
            if i == 0:
                G.add_node(t + 1)
            else:
                ProbDist.pop()
            second_node = np.random.choice(range(1, t+1), 1, ProbDist)[0]
            G.add_edge(t+1, second_node)
            second_nodes.append(second_node)
            ProbDists.append(ProbDist)

        if verbose >= 1:
            print("Iteration t =", t)
            print("Vertices and probability of attachment:")
            for i, P in enumerate(ProbDists):
                print(i, {n : p for n, p in zip(range(1, t + 1), P)})
                print("Sum of probability distribution = ", sum(P), "| selected vertex :", second_nodes[i])
            print("Randomly picked vertex/vertices for attachment:", second_nodes)
            print()
        if verbose >= 2:
            visualisation.display_graph(G, save_file="")
            time.sleep(1.5)
    return G


# To run this model, uncomment the following:

# main()
# visualisation.visualise_dot()
