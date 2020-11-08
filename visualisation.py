import graphviz as gv
import plotly.graph_objects as go
import collections
import networkx as nx
import numpy as np


def display_graph(G, save_file=r".\hofstad_PA.dot"):
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
                        title='<br>Graph',
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


def visualise_dot(path=r".\hofstad_PA.dot"):
    '''
    Make a pdf from the .dot file and open it.

    :param path: Path from where to load the .dot file
    :return:     Nothing
    '''
    s = gv.Source.from_file(filename=path)
    s.view()
