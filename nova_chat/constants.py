from enum import Enum
from pydantic import BaseModel

AIIP = "localhost"
PORT = "11434"

def get_url(ip: str, port: str):
    return f"{ip}:{port}"

class LLMConfig(BaseModel):
    model: str
    base_url: str

class RemoteLLM(Enum):
    LLAMA2 = LLMConfig(
        model="llama2:13b",
        base_url=get_url(AIIP, PORT)
    )