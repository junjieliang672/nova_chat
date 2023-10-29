from enum import Enum
from pydantic import BaseModel

AIIP = "localhost"
PORT = "11434"

def get_url(ip: str = AIIP, port: str = PORT):
    return f"http://{ip}:{port}"

class LLMConfig(BaseModel):
    model: str
    base_url: str
    label: str

class RemoteLLM(Enum):
    LLAMA2_13B = LLMConfig(
        model="llama2:13b",
        base_url=get_url(AIIP, PORT),
        label="ollama-llama2-13b",
    )
    LLAMA2_70B = LLMConfig(
        model="llama2:70b",
        base_url=get_url(AIIP, PORT),
        label="ollama-llama2-70b",
    )
    CODELLAMA = LLMConfig(
        model="codellama",
        base_url=get_url(AIIP, PORT),
        label="ollama-codellama-7b",
    )
    
    @classmethod
    def get_enum_by_model(cls, label_to_match: str):
        for item in cls:
            if item.value.label == label_to_match:
                return item