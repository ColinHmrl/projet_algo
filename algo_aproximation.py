import networkx as nx
import matplotlib.pyplot as plt

def aproximation_algorithm(matrix_coordonate, random_cities, n, matrix_city_completed):
    G = nx.Graph()
    for node in random_cities:
        G.add_nodes_from(random_cities)

    G = nx.complete_graph(random_cities)  # graph with a vertex for each city
    # for convenience, pick the city (x,y)-coordinates at random
    import random

    my_pos = { i : ( matrix_coordonate[i][0], matrix_coordonate[i][1] ) for i in random_cities } # pos[i] = (x_i, y_i)


    import math
    def eucl_dist(x1,y1,x2,y2):
        return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )

    for i,j in G.edges:
        (x1,y1) = my_pos[i]
        (x2,y2) = my_pos[j]
        G.edges[i,j]['length'] = matrix_city_completed[i][j]
    # find minimum spanning tree
    T = nx.minimum_spanning_tree(G,weight='length')

    # double (or bi-direct) the minimum spanning tree
    D = nx.DiGraph(T)
    # find an Eulerian cycle of the doubled spanning tree
    initial_tour = list( nx.eulerian_circuit(D,source=random_cities[0]))
    print(initial_tour)
    # take shortcuts (avoid repeated nodes)
    tour = [ random_cities[0] ]
    for (i,j) in initial_tour:
        if j not in tour:
            tour.append(j)
    total_circuit_l = 0
    for i in range(len(tour)):
        total_circuit_l += G.edges[initial_tour[i][0],initial_tour[i][1]]['length']
    print(total_circuit_l)

    # draw the tour
    tour_edges = [ (tour[i-1],tour[i]) for i in range(n) ]
    nx.draw(G.edge_subgraph(tour_edges), pos=my_pos)

    return initial_tour, total_circuit_l