from dijkstar import Graph, find_path
import random
import numpy as np



def convert_graph(graph):
  graph_dijkstra = Graph()
  for i in range(len(graph)):
    for j in range(len(graph)):
      graph_dijkstra.add_edge(i, j,graph[i][j])
  return graph_dijkstra



def input_output_contrainte(matrice, max_value):
    for i,line in enumerate(matrice):
        arr = np.where(line == np.inf)[0]
        arr = np.delete(arr,np.where(arr == i))
        while len(arr) > len(matrice)-3:
            index = random.choice(arr)
            matrice[i][index] = random.randint(1,max_value)
            arr = np.delete(arr,np.where(arr == index))
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] != np.inf:
                matrice[j][i] = matrice[i][j]
    return matrice


#Génère une matrice aléatoire de taille n
def gen_graph(size, max_value, prob):
    matrice = np.ones((size,size))*np.inf
    for i in range(size):
        for j in range(size):
            if random.uniform(0,1)<prob:
                matrice[i][j] = random.randint(1,max_value)
                matrice[j][i] = matrice[i][j]
            if j == i:
                matrice[i][i] = np.inf
    input_output_contrainte(matrice, max_value)
    return matrice



def random_city(graph, nb_city):
    if (nb_city <= len(graph)):
        return random.sample(range(len(graph)),nb_city)





def cities_complet(graph, cities):
    graph_cities = np.zeros((len(cities),len(cities)))
    graph_dji = convert_graph(graph)
    for index_city, city in enumerate(cities):
        for index_city2, city2 in enumerate(cities):
            graph_cities[index_city][index_city2] = graph[city][city2]
    for index, city in enumerate(graph_cities):
        liaisons = np.where(city == np.inf)
        liaisons = np.delete(liaisons,np.where(liaisons[0] == index))
        for col in liaisons:
            shortest_path = find_path(graph_dji,cities[index],cities[col])
            graph_cities[index][col] = shortest_path.total_cost
    for i in range(len(cities)):
        graph_cities[i][i] = 0
    return graph_cities



def gen_random(size_graph,size_cities, max_value, prob):
    """_summary_

    Args:
        size_graph (int): taille du graph de toutes les villes
        size_cities (int): taille des vilels par lesquels il faut passer
        max_value (int): valeur max des poids Xij
        prob (float): probabilité d'une connection entre 2 villes

    Returns:
        graph: _description_
    """
    graph = gen_graph(size_graph,max_value,prob)
    cities = random_city(graph,size_cities)
    cities_c = cities_complet(graph, cities)


    return graph,cities,cities_c


