import pickle


def import_dataset(name):
    with open(name+".pickle", "rb") as file:
        data = pickle.load(file)
    return data[0], data[1], data[2]

def export_dataset(name,graphe_complet, cities, cities_coordonates):
    data = [graphe_complet, cities, cities_coordonates]
    with open(name+".pickle", "wb") as file:
        pickle.dump(data, file)