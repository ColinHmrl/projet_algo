import pulp
from scipy.spatial import distance_matrix
from matplotlib import pyplot as plt
import time
import copy

#This function takes locations as input and plot a scatter plot
def plot_fig(loc,heading="plot"):
    plt.figure(figsize=(10,10))
    for i,row in loc.iterrows():
        if i==0:
            plt.scatter(row["x"],row["y"],c='r')
            plt.text(row["x"]+0.2, row["y"]+0.2, 'DELHI (depot) ')
        else:
            plt.scatter(row["x"], row["y"], c='black')
            plt.text(row["x"] + 0.2, row["y"] + 0.2,full_data.loc[i]['CITy'] )
        plt.ylim(6,36)
        plt.xlim(66,96)
        plt.title(heading)
# this function find all the subtour in the LP solution.
def get_plan(r0):
    r=copy.copy(r0)
    route = []
    while len(r) != 0:
        plan = [r[0]]
        del (r[0])
        l = 0
        while len(plan) > l:
            l = len(plan)
            for i, j in enumerate(r):
                if plan[-1][1] == j[0]:
                    plan.append(j)
                    del (r[i])
        route.append(plan)
    return(route)

def prog_lineaire(graph_complet_cities, random_cities):
    """_summary_

    Args:
        graphe : graphe complet de liste   
        random_cities : liste de villes séléctionnées

    Returns:
        route_plan: liste de la route
        subtour: liste des subtours
        time_taken: temps de calcul
        status : Statut de l'opti
        value : Valeur de l'objectif
    """
    no_of_locs = len(graph_complet_cities)

    dis_mat = graph_complet_cities

    start_t_1=time.time()
    model=pulp.LpProblem('tsp',pulp.LpMinimize)
    #define variable
    x=pulp.LpVariable.dicts("x",((i,j) for i in range(no_of_locs)for j in range(no_of_locs)),cat='Binary')
    #set objective
    model+=pulp.lpSum(dis_mat[i][j]* x[i,j] for i in range(no_of_locs) for j in range(no_of_locs))
    # st constraints
    for i in range(no_of_locs):
        model+=x[i,i]==0
        model+=pulp.lpSum(x[i,j] for j in range(no_of_locs))==1
        model+=pulp.lpSum(x[j, i] for j in range(no_of_locs)) == 1
    status=model.solve()
    route=[(i,j) for i in range(no_of_locs) for j in range(no_of_locs) if pulp.value(x[i,j])==1]
    route_plan=get_plan(route)
    subtour=[]
    while len(route_plan)!=1:
        for i in range(len(route_plan)):
            model+=pulp.lpSum(x[route_plan[i][j][0],route_plan[i][j][1]]for j in range(len(route_plan[i])))<=len(route_plan[i])-1
        status=model.solve()
        route = [(i, j) for i in range(no_of_locs) for j in range(no_of_locs) if pulp.value(x[i, j]) == 1]
        route_plan = get_plan(route)
        subtour.append(len(route_plan))

    for i in range(len(route_plan[0])):
        temp_list = list(route_plan[0][i])
        temp_list[0], temp_list[1] = random_cities[route_plan[0][i][0]], random_cities[route_plan[0][i][1]]
        route_plan[0][i] = tuple(temp_list)

    return route_plan,subtour,time.time()-start_t_1,pulp.LpStatus[status],pulp.value(model.objective)


def get_borne_inf(graph_complet_cities, random_cities):
    print(prog_lineaire(graph_complet_cities, random_cities)[-1])