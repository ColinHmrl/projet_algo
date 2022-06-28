import numpy as np
import random
import time


def random_matrice_pondere(size,max_wheight,seed=5):
    """Génère un graph complet pondéré aléatoirement.

    Args:
        size (int): nombre de nodes dans un graph.
        max_wheight (_type_): valeure maximale des poids des edges.
        seed (int, optional): Seed pour le random. Defaults to 5. None to random.

    Returns:
        matrice: matrice de size*size pondérée de type numpy.array
    """
    np.random.seed(seed)
    matrice = np.random.random_sample((size,size)) * max_wheight
    for i in range(size):
        matrice[i][i] = np.nan
        for j in range(size):
            matrice[i][j] = matrice[j][i]

    return matrice

def random_path_generator(size,seed=None):
    """Génère un chemin aléatoire parmis une taille de nodes.

    Args:
        size (int): _description_
        seed (int, optional): Seed pour le random. Defaults to 5.

    Returns:
        ndarray: list de taille size contenant des valeurs entre 0 et size-1.
    """

    np.random.seed(seed)
    path = np.random.permutation(size)
    return np.append(path, path[0])

def path_to_matrice(path,wheight=1):
    """Transfert un chemin en matrice.

    Args:
        path (list): path
        wheight (int, optional): Valeure assignée aux poids. Defaults to 1.

    Returns:
        matrice: matrice des chemins
    """

    size = len(path)
    matrice = np.zeros((size,size))
    for value in range(0,len(path)-1):
        matrice[path[value]][path[value+1]] = wheight

    return matrice

def path_distance(path,matrice):
    """Calcule la distance d'un chemin.

    Args:
        path (list): path
        matrice (numpy.array): matrice des poids

    Returns:
        float: distance du chemin
    """

    distance = 0
    for i in range(len(path)-1):
        distance += matrice[path[i]][path[i+1]]
    return distance

def calcul_path_pheromone(pheromone,size,start):
    """créé un chemin à partir d'un résultat de l'algorithme ACO
    """
    pheromone = np.nan_to_num(pheromone)
    final_path= [start]
    position = start
    for x in range(size-1):
        
        pheromone[:,position] = 0
        #print(res)
        position = np.argmax(pheromone[position])
        final_path.append(position)
    final_path.append(start)
    return final_path

def path_edge_selection(pheromone,matrice,start,alpha,beta):
    """Path edge selection pour l'aco

    Args:
        pheromone (numpy.array): array if pheromones
        matrice (numpy.array): matrice du path
        start (int): point de départ
        alpha (float): facteur de quantité de pheromone
        beta (float): facteur de désirabilité lié a la rapidité / distance de l'edge

    Returns:
        ndarray: path from start in pheromone/matrice
    """

    path = [start]
    nodes = range(len(pheromone))

    for rep in range(len(pheromone)-1):
        nodes_availables = [node for node in nodes if( (node not in path))]
        
        weigths_node = [pheromone[path[-1]][y] ** alpha * (1/matrice[path[-1]][y]) ** beta for y in nodes_availables]
        probas_nodes = [weigths_node[y]/sum(weigths_node) for y in range(len(weigths_node))]
        
        path.append(random.choices(nodes_availables, weights=probas_nodes, k=1)[0])

    path.append(start)

    return path

def delta_T_xy_ant(paths_ant_matrice_wheight,x,y): 
    if paths_ant_matrice_wheight[x][y] == 0:
        return 0
    else:
        return 1/paths_ant_matrice_wheight[x][y]

def get_best_path(paths_ants,paths_ants_value):
    best_path =  paths_ants[np.argmax(paths_ants_value)]
    best_path_value = np.max(paths_ants_value)
    return best_path,best_path_value


def aco_algorithm(matrice, parameters,result):


    pheromone_matrice = random_matrice_pondere(len(matrice),0)
    best_path = path_edge_selection(pheromone_matrice,matrice,0,parameters["a"],parameters["b"])
    best_score = path_distance(best_path,matrice)

    time_record = []



    for x in range(parameters["nb_iter_max"]):

        #Création des fourmis
        start = time.time()

        ants_start = np.random.randint(0,len(matrice),parameters["nbr_ant"])
        paths_ants = [path_edge_selection(pheromone_matrice,matrice,start,parameters["a"],parameters["b"]) for start in ants_start]
        
        time_paths_ants = time.time()-start
        
        #calcule des poids des path des fourmis
        start = time.time()

        paths_ants_value = [path_distance(path,matrice) for path in paths_ants]

        time_paths_ants_value = time.time()-start

        #calcule des 
        start = time.time()

        paths_ants_matrice_wheight = [path_to_matrice(paths_ants[index],paths_ants_value[index]) for index in range(len(paths_ants))]

        time_paths_ants_matrice_wheight = time.time()-start

        start = time.time()

        for i in range(len(matrice)):
            for j in range(len(matrice)):

                pheromone_matrice[i][j] = (1 - parameters["p"]) * pheromone_matrice[i][j] + sum(delta_T_xy_ant(paths_ant_matrice_wheight,i,j) for paths_ant_matrice_wheight in paths_ants_matrice_wheight)

        time_pheromone_matrice = time.time()-start

        #print("iteration : ",x,"/",nbr_iter,"\n","time_paths_ants : ",time_paths_ants,"\n","time_paths_ants_value : ",time_paths_ants_value,"\n","time_paths_ants_matrice_wheight : ",time_paths_ants_matrice_wheight,"\n","time_pheromone_matrice : ",time_pheromone_matrice)

        best_path,best_score = get_best_path(paths_ants,paths_ants_value)
        time_record.append([time_paths_ants,time_paths_ants_value,time_paths_ants_matrice_wheight,time_pheromone_matrice])

    result.append((pheromone_matrice,best_path,best_score,time_record))


###
#
#


