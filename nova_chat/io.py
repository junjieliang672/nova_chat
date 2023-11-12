import os
import pickle
from nova_chat.constants import IO_DIR

def save_message(filename, mes):
    p = os.path.join(IO_DIR, filename)
    print(p)
    with open(p, 'wb') as file:
        pickle.dump(mes, file)

def load_message(filename):
    p = os.path.join(IO_DIR, filename)
    print(p)
    with open(p, "rb") as file:
        return pickle.load(file)