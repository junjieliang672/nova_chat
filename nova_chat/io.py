import os
import json
from nova_chat.constants import IO_DIR

def memory_to_dict(memory):
    return [msg.dict() for msg in memory.chat_memory.messages]

def save_message(filename, mes):
    p = os.path.join(IO_DIR, filename)
    with open(p, 'w') as file:
        json.dump(mes, file)

def load_message(filename):
    p = os.path.join(IO_DIR, filename)
    with open(p, "r") as file:
        return json.load(file)