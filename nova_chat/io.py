import os
import pickle

def save_message(p, mes):
    with open(p, 'wb') as file:
        pickle.dump(mes, file)
    return p

def load_message(p):
    with open(p, "rb") as file:
        return pickle.load(file)
    
def delete_message(p):
    if os.path.exists(p):
        os.remove(p)