def PA_model2(G, delta, m, t, t_stop=10, verbose=True, num_iterations):
    '''
    Recursively simulate a Preferential Attachment model using the Hofstad model as basis. A decision rule is added,
    which decides whether we use a vertex-step or an edge-step. The vertex step adds a new vertex to G, selects another
    vertex with probability P (= degree of u/sum of all degrees in G) and adds an edge between these vertices. The edge-
    step selects two vertices from G with the same probability P for each vertex and adds an edge between these.


    :param G:       The Graph that is used for simulating Hofstad's model
    :param delta:   An affine attachment rule parameter
    :param m:       Number of edges that are attached to a new vertex
    :param t:       The current timestep of the simulation
    :param t_stop:  The timestep after which to stop the simulation
    :param verbose: Whether to print a verbose output of the simulation, including visualising graph G
    :return:
    '''
    Z = []
    p = 2 - np.sqrt(3)
    Z.append(bernoulli.rvs(p, size = num_iterations))
    if i in Z:
        np.random.choice([0, 1])

    ProbabilityVertexPick = []
    sum_degrees = 0
    for i in G.nodes():
        sum_degrees += G.degree(i)

    for j in G.nodes():
        ProbabilityVertexPick.append(G.degree(j) / sum_degrees)
    G.add_node(t+1)

    if #decision rule:
        G.add_node()

