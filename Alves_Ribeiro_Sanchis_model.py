import numpy as np
import time
from scipy.stats import bernoulli
import visualisation

# Define edge step functions
def edgeStepFun1(t):  # 1/linear function
    return 1 / (t ** 1.01)


def edgeStepFun2(t):  # 1/log-squared function (base 2)
    return 1 / (np.log2(t)**2)


def edgeStepFun3(t):  # 1/log-function (base 2)
    return 1 / np.log2(t)


def model_edgestepfunc(G, m, edgestepfun, t, t_stop=10, verbose=0):
    '''
    Recursively simulate a Preferential Attachment model using the Hofstad model as basis. A decision rule is added,
    which decides whether we use a vertex-step or an edge-step. The vertex step adds a new vertex to G, selects another
    vertex with probability P (= degree of u/sum of all degrees in G) and adds an edge between these vertices. The edge-
    step selects two vertices from G with the same probability P for each vertex and adds an edge between these.

    :param G:       The Graph that is used for simulating Hofstad's model
    :param m:       Number of edges that are attached to a new vertex
    :param p:       Bernouilli probability
    :param t_stop:  The timestep after which to stop the simulation
    :param verbose: Whether to print a verbose output of the simulation, including visualising graph G
    :return:
    '''

    # Determine whether we make edge-step or vertex-step
    edge_steps_taken = 0

    for t in range(t, t_stop):
        p = edgestepfun(t)
        Z_t = bernoulli.rvs(p, size=1)[0]
        ProbDists = []
        first_nodes = []
        second_nodes = []
        if Z_t == 1:
            for i in range(m):
                ProbabilityVertexPick = []
                sum_degrees = 2 * t * m + i
                for j in G.nodes():
                    ProbabilityVertexPick.append(G.degree(j) / sum_degrees)
                if i == 0:
                    G.add_node(t + 1)
                else:
                    ProbabilityVertexPick.pop()
                second_node = np.random.choice([n for n in G.nodes if n != t + 1], 1, ProbabilityVertexPick)[0]
                G.add_edge(t + 1, second_node)
                ProbDists.append(ProbabilityVertexPick)
                second_nodes.append(second_node)

        elif Z_t == 0:
            for i in range(m):
                ProbabilityVertexPick = []
                sum_degrees = 2 * t * m + 2 * i
                for j in G.nodes():
                    ProbabilityVertexPick.append(G.degree(j) / sum_degrees)
                first_node = np.random.choice(G.nodes, 1, ProbabilityVertexPick)[0]
                second_node = np.random.choice(G.nodes, 1, ProbabilityVertexPick)[0]
                while first_node == second_node:
                    second_node = np.random.choice(G.nodes, 1, ProbabilityVertexPick)[0]
                G.add_edge(first_node, second_node)
                ProbDists.append(ProbabilityVertexPick)
                first_nodes.append(first_node)
                second_nodes.append(second_node)
            edge_steps_taken += 1

        if verbose >= 1:
            print("Iteration t =", t)
            print("p =", p)
            if Z_t == 1:
                print("Vertex step taken.")
            elif Z_t == 0:
                print("Edge step taken.")
            print("Vertices and probability of attachment:")
            for i, P in enumerate(ProbDists):
                print(i, {n: p for n, p in zip(range(1, t + 1), P)})
                if Z_t == 1:
                    print("Sum of probability distribution = ", sum(P), "| selected vertex :",
                          second_nodes[i])
                elif Z_t == 0:
                    print("Sum of probability distribution = ", sum(P), "| selected vertices :",
                          first_nodes[i], second_nodes[i])
            if Z_t == 1:
                print("Randomly picked vertex/vertices for attachment:", second_nodes)
            elif Z_t == 0:
                print("Randomly picked vertex/vertices for attachment:",
                      [(f, s) for f, s in zip(first_nodes, second_nodes)])
            print()
        if verbose >= 2:
            visualisation.display_graph(G, save_file="")
            time.sleep(1.5)
    return G
