
import matplotlib.pyplot as plt
import statistics
import numpy as np

def histogramme(bornes, pins):
    plt.hist(bornes, bins=pins, edgecolor = "black")                         
    plt.xlabel("distance à la borne (pourcentage)")               
    plt.ylabel("nombre d'intances")                               
    plt.title("Distribution des distances à la borne supérieure") 

    
def courbe(iterations_max, sol_courante, sol_best):
    plt.plot(range(iterations_max), sol_courante)
    plt.plot(range(iterations_max), sol_best)
    plt.xlabel("nb itérations", fontsize=16)
    plt.ylabel("valeur", fontsize=16)


def courbe_stats(bornes, debut, fin, pas):
    moyennes = []
    deviations = []
    moyennes.append(statistics.fmean(bornes))               
    deviations.append(np.std(bornes))
    plt.plot(range(debut, fin, pas), moyennes)
    # affichage de la bande d'écart-type
    plt.fill_between(range((debut, fin, pas),
                    np.subtract(moyennes, deviations), # borne haute
                    np.add(moyennes, deviations),      # borne basse
                    alpha=.1))                     
    plt.xlabel("taille de la liste tabou")
    plt.ylabel("distance à la borne")
    plt.title("Impact de la taille de la liste tabou sur la qualité des solutions")
    plt.show()                       


