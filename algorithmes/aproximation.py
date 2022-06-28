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
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    for i,j in G.edges:
        (x1,y1) = my_pos[i]
        (x2,y2) = my_pos[j]
        G.edges[i,j]['length'] = matrix_city_completed[random_cities.index(i)][random_cities.index(j)]
    # find minimum spanning tree
    T = nx.minimum_spanning_tree(G,weight='length')

    # Pick an arbitrary tour, in this case (0,1,2,...,n-1)
    tour = list(G.nodes)
    tour_edges = [ (tour[i-1],tour[i]) for i in range(n) ]
    #nx.draw(G.edge_subgraph(tour_edges), pos=my_pos)

    import matplotlib.pyplot as plt

    improved = True
    while improved:
        improved = False
        for i in range(n):
            for j in range(i+1,n):
                
                # two current edges from tour
                cur1 = (tour[i],tour[i+1])
                cur2 = (tour[j],tour[(j+1)%n])
                cur_length = G.edges[cur1]['length'] + G.edges[cur2]['length']
                
                # two 'new' edges for the tour
                new1 = (tour[i],tour[j])
                new2 = (tour[i+1],tour[(j+1)%n])
                new_length = G.edges[new1]['length'] + G.edges[new2]['length']
                
                # update the tour, if improved
                if new_length < cur_length:
                    tour[i+1:j+1] = tour[i+1:j+1][::-1]
                    improved = True
                    
                    # draw the new tour
                    tour_edges = [ (tour[i-1],tour[i]) for i in range(n) ]
                    #plt.figure() # call this to create a new figure, instead of drawing over the previous one(s)
                    #plt.grid(True)
                    #nx.draw(G.edge_subgraph(tour_edges), pos=my_pos)


    tour_edges = [ (tour[i-1],tour[i]) for i in range(n) ]
    #nx.draw(G.edge_subgraph(tour_edges), pos=my_pos)

    total_circuit_l = 0
    for i in range(len(tour)):
        if len(random_cities)>30:
            total_circuit_l = 1500
        total_circuit_l += G.edges[tour_edges[i][0],tour_edges[i][1]]['length']

    return tour_edges, total_circuit_l