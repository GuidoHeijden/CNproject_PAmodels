from scipy.stats import bernoulli

def PA_model2(G, m, p, t_stop, num_iterations):
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

    # Create list with Bernoulli random variables 0 and 1 based on probability p
    Z = []
    Z.append(bernoulli.rvs(p, size=num_iterations))

    # Determine whether we make edge-step or vertex-step
    ProbDists = []
    first_nodes = []
    second_nodes = []
    ProbabilityVertexPick = []

    for t in range(2, t_stop):
        for l in range(m):
            for i in Z:
                if i==1:
                    sum_degrees = 0
                    for k in G.nodes():
                        sum_degrees += G.degree(k)
                    for j in G.nodes():
                        ProbabilityVertexPick.append(G.degree(j) / sum_degrees)
                    G.add_node(t+1)
                    second_node = np.random.choice(range(1, t+2), 1, ProbDist)[0]
                    G.add_edge(t+1, second_node)
                    ProbDists.append(ProbDist)
                    second_nodes.append(second_node)
                elif i==0:
                    sum_degrees = 0
                    for k in G.nodes():
                        sum_degrees += G.degree(k)
                    for j in G.nodes():
                        ProbabilityVertexPick.append(G.degree(j) / sum_degrees)
                    first_node = np.random.choice(range(1, t+2), 1, ProbDist)[0]
                    second_node = np.random.choice(range(1, t+2), 1, ProbDist)[0]
                    G.add_edge(first_node, second_node)
                    ProbDists.append(ProbDist)
                    second_nodes.append(second_node)