from pulp import *
import numpy as np
import random
from dijkstar import Graph, find_path

# Creation d'une ville sur une carte donnée
def generate_nodes(number,max_x=1080,max_y=720):
    """
    Créer une liste de villes sous forme de coordonnées
    
    Parameters
    ----------
    number : int
        Nombre de ville a générer sur la carte
    max_x : int, optional
        Maximum de la largeur de la carte. The default is 1080.
    max_y : int, optional
        Maximum de la hauteur de la carte. The default is 720.
    """
    # Initialisation de la liste de villes
    nodes = []
    # Boucle pour générer les villes
    for i in range(number):
        # Génération des coordonnées de la ville
        nodes.append([random.randint(0.1*max_y,max_x-0.1*max_y),random.randint(0.1*max_y,max_y-0.1*max_y)])

    return nodes



# Retourne la distance entre 2 points (x1,y1) et (x2,y2)
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5



# Retourne la matrice de distance entre les villes
def coordinats_to_matrice(nodes,prob):
    """
    Créer une matrice de distance entre les villes
    
    Parameters
    ----------
    nodes : list
        Liste de villes
    """
    matrice = np.ones((len(nodes),len(nodes)))*np.inf
    for x in range(len(nodes)):
        for y in range(len(nodes)):
            if random.uniform(0,1)<prob:
                matrice[x][y] = distance(nodes[x][0],nodes[x][1],nodes[y][0],nodes[y][1])
                matrice[y][x] = matrice[x][y]
            if x == y :
                matrice[x][x] = np.inf
    return matrice



# Génère une liste de villes par lesquels passer 
def random_city(graph, nb_city):
    if (nb_city <= len(graph)):
        return random.sample(range(len(graph)),nb_city)



# Convertit le graphe en format de dijkstra
def convert_graph(graph):
    graph_dijkstra = Graph()
    for i in range(len(graph)):
        for j in range(len(graph)):
            graph_dijkstra.add_edge(i, j,graph[i][j])
    return graph_dijkstra



# Génère le graphe complet des villes séléctionnées
def cities_complet(graph, cities, format_is_inf):
    """
    Créer un graphe complet des villes séléctionnées

    Parameters
    ----------
    graph : list
        Graphe des distances entre les villes
    cities : list
        Liste de villes séléctionnées
    """
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
    if format_is_inf == False:
        for i in range(len(cities)):
            graph_cities[i][i] = 0
    return graph_cities




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



# Génère toutes le dataset d'une instance
def random_matrix_generator(size_graph,size_cities, max_value_x, max_value_y, prob, format_is_inf=True):
    """
    Génère toutes les matrices d'une instance

    Parameters
    ----------
    size_graph : int
        Taille du graphe
    size_cities : int
        Taille des villes
    max_value : int
        Valeur maximale des distances
    prob : float
        Probabilité de la distance infini
    complet_is_inf : bool, optional
        True si le format de sortie du graphe complet doit être infini. The default is False.
    """
    # Génération des villes
    matrix_coordonate = generate_nodes(size_graph,max_value_x,max_value_y)
    # Génération de la matrice de distance
    matrix_distance = coordinats_to_matrice(matrix_coordonate,prob)
    # Génération si full 0 sur la ligne
    matrix_distance = input_output_contrainte(matrix_distance, max_value_x)
    # Création de la liste des villes
    random_cities = random_city(matrix_distance,size_cities)
    # Génération du graphe complet
    city_completed = cities_complet(matrix_distance, random_cities, format_is_inf)

    return matrix_coordonate, matrix_distance, random_cities, city_completed