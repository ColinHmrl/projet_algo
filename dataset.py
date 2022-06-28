import pickle


def import_dataset(name):
    with open(name+".pickle", "rb") as file:
        data = pickle.load(file)
    return data

def export_dataset(name,data):
    with open(name+".pickle", "wb") as file:
        pickle.dump(data, file)