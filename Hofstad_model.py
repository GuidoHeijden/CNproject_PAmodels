import networkx as nx
import graphviz as gv
import pydot as pyd
import plotly.graph_objects as go
import time
import numpy as np
import collections

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
    display_graph(G)


def display_graph(G, save_file=r"C:\Users\Mariya Karlashchuk\Documents\Studie\Complex Networks\Project\hofstad_PA.dot"):
    '''
    This function displays a graph G using the Kamada-Kawai layout. Plotly is used for visualisation, but it is possible
    to save a .dot file of the graph. Self-loops and multiple edges between the same two vertices can be displayed
    correctly, and the vertices are color-coded according to their degree.

    :param G:           The graph to display
    :param save_file:   Where to save a .dot file of the graph (make this an empty string to not save the graph)
    :return:            Nothing
    '''
    # Set up the layout of the graph
    pos = nx.kamada_kawai_layout(G)
    nx.set_node_attributes(G, pos, "pos")

    # Start by drawing all the edges
    edge_x = []
    edge_y = []
    self_loop_x = []
    self_loop_y = []
    arched_x = []
    arched_y = []
    edge_counter = collections.Counter(G.edges())
    for edge in set(G.edges()):
        if edge[0] != edge[1]:
            num_this_edge = edge_counter[edge]
            # Straight edge
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            if num_this_edge % 2 == 1:
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)

            # Arched edges
            if num_this_edge >= 2:
                angle  = np.arctan2(y1-y0, x1-x0) * 180 / np.pi
                x_center = (x1-x0)/2 + x0
                y_center = (y1-y0)/2 + y0
                x_disp = np.cos(np.pi*(angle-90)/180)
                y_disp = np.sin(np.pi*(angle-90)/180)
                arch_scalar = np.linalg.norm(np.array([x0, y0])-np.array([x1, y1])) / 8
                for edge_iter in range(num_this_edge // 2):
                    # First arch
                    arched_x.append(x0)
                    arched_x.append(x_center+x_disp*arch_scalar*(edge_iter+1))
                    arched_x.append(x1)
                    arched_x.append(None)
                    arched_y.append(y0)
                    arched_y.append(y_center+y_disp*arch_scalar*(edge_iter+1))
                    arched_y.append(y1)
                    arched_y.append(None)
                    # Second arch
                    arched_x.append(x0)
                    arched_x.append(x_center-x_disp*arch_scalar*(edge_iter+1))
                    arched_x.append(x1)
                    arched_x.append(None)
                    arched_y.append(y0)
                    arched_y.append(y_center-y_disp*arch_scalar*(edge_iter+1))
                    arched_y.append(y1)
                    arched_y.append(None)

        # Self-loops
        else:
            num_self_loops = edge_counter[edge]
            x, y = G.nodes[edge[0]]['pos']
            loop_scalar = 0.1  # Manipulate the size radius of the self-loop
            circle_precision = 15  # Number of points in circle trace (divided by 2)
            for loop_iter in range(num_self_loops):
                x_circle = [x + loop_scalar*(1+loop_iter*0.25)/2 + np.cos(i)*loop_scalar*(1+loop_iter*0.25)/2 for i in np.arange(0, 2 * np.pi + 0.0001, np.pi / circle_precision)]
                y_circle = [y +                                  + np.sin(i)*loop_scalar*(1+loop_iter*0.25)   for i in np.arange(0, 2 * np.pi + 0.0001, np.pi / circle_precision)]
                self_loop_x += x_circle
                self_loop_x.append(None)
                self_loop_y += y_circle
                self_loop_y.append(None)

    # Traces for straight edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Traces for arched edges
    arched_edge_trace = go.Scatter(
        x=arched_x, y=arched_y,
        mode="lines",
        line=dict(shape='spline', color='#888', width=0.5),
        hoverinfo='none',
        showlegend=False)

    # Traces for self loops
    self_loops_trace = go.Scatter(
        x=self_loop_x, y=self_loop_y,
        mode="lines",
        line=dict(shape='spline', color='#888', width=0.5),
        hoverinfo='none',
        showlegend=False)

    # Draw the nodes
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Calculate and visualise the degree of each node
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append("Vertex " + str(node) + '; # of connections: ' + str(len(adjacencies[1])))
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Create graph figure without self_loops
    fig = go.Figure(data=[edge_trace, self_loops_trace, node_trace, arched_edge_trace],
                    layout=go.Layout(
                        title='<br>Hofstad graph',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        # annotations=[dict(
                        #     text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        #     showarrow=False,
                        #     xref="paper", yref="paper",
                        #     x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    # fig.add_trace(self_loops_trace)  # Add self-loops
    fig.show()

    # Also save the graph as dot file
    if save_file != "":
        nx.drawing.nx_pydot.write_dot(G, save_file)


def visualise_dot(path=r"C:\Users\Mariya Karlashchuk\Documents\Studie\Complex Networks\Project\hofstad_PA.dot-"):
    '''
    Make a pdf from the .dot file and open it.

    :param path: Path from where to load the .dot file
    :return:     Nothing
    '''
    s = gv.Source.from_file(filename=path)
    s.view()


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
        P = []
        for n in G.nodes():
            P.append( (G.degree(n) + delta) / (t*(2*m + delta) + (m + delta)) )
        G.add_node(t+1)
        P.append( (m + delta) / (t*(2*m + delta) + (m + delta)) )
        second_nodes = []
        for i in range(m):
            second_node = np.random.choice(range(1, t+2), 1, P)[0]
            G.add_edge(t+1, second_node)
            second_nodes.append(second_node)

        if verbose >= 1:
            print("Iteration t =", t)
            print("Vertices and probability of attachment:\n", {n : p for n, p in zip(range(1, t + 2), P)})
            print("Randomly picked vertex/vertices for attachment:", second_nodes)
            print("Sum of probability distribution = ", sum(P))
            print()
        if verbose >= 2:
            display_graph(G, save_file="")
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

# TODO : fix this function since G.degree does not give the correct degree for self-loops (does that also matter here?)
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
        P = []
        for n in G.nodes():
            P.append( (G.degree(n) + delta) / (t*(2*m + delta)) )
        G.add_node(t+1)
        second_nodes = []  # used for verbose output
        for i in range(m):
            second_node = np.random.choice(range(1, t+1), 1, P)[0]
            G.add_edge(t+1, second_node)
            second_nodes.append(second_node)

        if verbose >= 1:
            print("Iteration t =", t)
            print("Vertices and probability of attachment:\n", {n : p for n, p in zip(range(1, t + 2), P)})
            print("Randomly picked vertex/vertices for attachment:", second_nodes)
            print("Sum of probability distribution = ", sum(P))
            print()
        if verbose >= 2:
            display_graph(G, save_file="")
            time.sleep(1.5)
    return G

# Define edge step functions
def edgeStepFun1(t): # 1/linear function
    return 1 / (t ^ 1.01)

def edgeStepFun2(t): # 1/log-squared function
    return 1 / (np.log(t)**2)

def edgeStepFun3(t): # 1/log-function
    return 1 / log(t)

main()
visualise_dot()
