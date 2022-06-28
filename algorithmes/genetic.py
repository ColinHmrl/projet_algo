# %%
import random
import numpy as np

# %%
def generate_nodes(number,max_x=1080,max_y=720,seed=None):
    # create number of nodes with coordinates of x,y  with max value of 600
    random.seed(seed)
    nodes = []
    for i in range(number):
        nodes.append([random.randint(0.1*max_y,max_x-0.1*max_y),random.randint(0.1*max_y,max_y-0.1*max_y)])
    return nodes

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def coordinats_to_matrice(nodes):
    # create a matrice with the nodes coordinates
    matrice = np.zeros((len(nodes),len(nodes)))
    for x in range(len(nodes)):
        for y in range(len(nodes)):
            matrice[x][y] = distance(nodes[x][0],nodes[x][1],nodes[y][0],nodes[y][1])
    return matrice

# %%
parameters = {
    'nbr_sommet': 100,
    'nbr_indivudus':1000,
    'nbr_generation':1000,
    'prob_no_mutation':0.01,
    'prob_mutation_insertion':0.3,
    'prob_mutation_reversion':0.3,
    'prob_mutation_swap':0.3,
}

# %% [markdown]
# # Aglorithme génétique
# ## etapes de l'ago génétique:
# 1. Population de base générée aléatoirement
#    1. On génère une population de taille n. Il s'agit de chemins générer aléatoirement
# 2. Évaluation
#    1. On evalue notre population selon le critère du chemin le plus cours et respectant les contraintes
# 3. Sélection
#    1. Sélection retenue: tirage au sort de n/2 couples, proba pondéré par le score de chacun. Si le plus fort n'est pas sélectionné, il est automatiquement sélectionné dans la génération d'après pour remplacé un individu de la population. <- n/2 couples ça veut dire que l'on prends tous les individus et qu'on les fais se reproduire ensemble sans selection.
#    2. Selection de n/2 individus, formants n/4 couples, reproduction de ces indivus pour faire un brassage génétique. chaque individu 
# 4. Croisement et mutation
#    1. Crossover :
#       1. 123 456 et 254 316 donnent 2 enfants:
#          123 546 et 123 546
#    2. x % de chance de mutation par individu
#       on effectue une permutation de deux index : 123 546 peut devenir 132 546 ou encore 125 346
# 
# 
# ## paramètres
# 
# - nbr_generation
# - nbr_indivudus
# - 

# %%
def generate_path(nbr_sommet):
    # create a path with the nodes coordinates
    path = []
    for i in range(nbr_sommet):
        path.append(i)
    random.shuffle(path)
    return path

#generate_path(10)


def generate_population(nbr_indivudus,nbr_sommet):
    # create a population with the nodes coordinates
    population = []
    for i in range(nbr_indivudus):
        population.append(generate_path(nbr_sommet))
    return population

def evaluate_path(path,matrice):
    # calculate the fitness of a path
    fitness = 0
    for i in range(len(path)-1):
        fitness += matrice[path[i]][path[i+1]]
    fitness += matrice[path[-1]][path[0]]
    return fitness

def evaluate_population(population,matrice):
    # calculate the fitness of each individual
    evaluation = []
    for i in range(len(population)):
        
        evaluation.append(evaluate_path(population[i],matrice))
    return evaluation


def selection_population(population,evaluation):
    #ponderate the population with the fitness
    weighted_evaluation = []
    for i in range(len(population)):
        weighted_evaluation.append(1/(evaluation[i]**10))
    #print("len(population) ",len(population))
    parents = random.choices(population,weights=weighted_evaluation,k=int(len(population)/2))

    return parents

def crossover(parents,nbr_sommet):

    pivot = int(nbr_sommet/2)
    children = []
    for index_parent in range(0,len(parents),2):
        child = []
        child = parents[index_parent][:pivot]

        #print("len(child) ",len(child))

        for i in range(nbr_sommet):
            #print(index_parent,i)
            #print(index_parent+1,i)
            #print("len(parents) ",len(parents))
            if parents[index_parent+1][i] not in child:
                child.append(parents[index_parent+1][i]) 
#            print(child)
#            print("parent 1 : ",parents[index_parent])
#            print("parent 2 : ",parents[index_parent+1])
            
        children.append(child)
        children.append(child)
        children.append(child)
        children.append(child)

    return children


def mutation_insertion(path):
    #print("inversion")
    index_to_insert_into = random.randint(0,len(path)-1)
    index_to_insert = random.randint(0,len(path)-1)
    values_to_insert = path[index_to_insert]

    path.pop(index_to_insert)
    path.insert(index_to_insert_into,values_to_insert)
    return path

def mutation_swap(path):
    #print("swap")
    index_to_swap_1 = random.randint(0,len(path)-1)
    index_to_swap_2 = random.randint(0,len(path)-1)
    values_to_swap_1 = path[index_to_swap_1]
    values_to_swap_2 = path[index_to_swap_2]

    path[index_to_swap_1] = values_to_swap_2
    path[index_to_swap_2] = values_to_swap_1
    return path

def mutation_reversion(path):
    #print("reversion")
    max_len_reversion = int(len(path)/4)

    index = random.randint(0,len(path)-max_len_reversion)
    size = random.randint(1,max_len_reversion)
    #revert index_to_reversion to index_to_reversion+size_of_reversion in path
    reverted = []
    for i in range(index+size-1,index-1,-1):
        reverted.append(path[i])
#    print(reverted)
    for i in range(index,index+size):
        path[i] = reverted.pop(0)

    
#    print(index)
#    print(size)
    return path

def no_mutation(path):
    #print("no mutation")
    return path

def mutation_children(children,parameters):
    
    random.seed(None)
    children_mutated = []
    for child in children:
        fct = random.choices(
            population=[no_mutation,mutation_insertion,mutation_reversion,mutation_swap],
            weights=[
                parameters['prob_no_mutation'],
                parameters['prob_mutation_insertion'],
                parameters['prob_mutation_reversion'],
                parameters['prob_mutation_swap']],
            k=1)

        children_mutated.append(fct[0](child))

    #print("len(children ",len(children))
    #print("len(children_mutated) ",len(children_mutated))
    return children_mutated

# %%
def genetic_algorithme(matrice,parameters):
    #1.Population de base est générée aléatoirement
    population = generate_population(parameters['nbr_indivudus'],parameters['nbr_sommet'])

    best_path = population[0]
    best_path_value = evaluate_path(best_path,matrice)

    for generation in range(parameters["nbr_generation"]):
        #2.La population est évaluée
        evaluation = evaluate_population(population,matrice)
        
        #print(evaluation)
        idx_best_path = np.argmin(evaluation)
        if evaluate_path(population[idx_best_path],matrice) < best_path_value:
            best_path = population[idx_best_path]
            best_path_value = evaluate_path(population[idx_best_path],matrice)

        #3.Selection des parents
        parents = selection_population(population,evaluation)


        #4.Création des enfants
        children = crossover(parents,parameters['nbr_sommet'])
        
        #5.Mutation des enfants
        children = mutation_children(children,parameters)

        print("#############")
        print("Generation :",generation)
        print("Best path :",best_path)
        print("Best path value :",best_path_value)
        #print("Parents :",parents)
        #print("children :",children)
        print("#############")
        population = children

    return best_path_value
        