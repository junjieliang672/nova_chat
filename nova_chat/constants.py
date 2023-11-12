from enum import Enum
from typing import Optional
from pydantic import BaseModel
from os import environ

AIIP = "localhost"
PORT = "11434"

def get_url(ip: str = AIIP, port: str = PORT):
    return f"http://{ip}:{port}"

class LLMConfig(BaseModel):
    model: str
    base_url: Optional[str]
    label: Optional[str]
    open_api_key: Optional[str] = None

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
    CHATGPT_16K = LLMConfig(
        model="gpt-3.5-turbo-16k",
        base_url=None,
        label="chatgpt-16k",
        open_api_key=environ.get("OPENAI_API_KEY"),
    )
    CHATGPT = LLMConfig(
        model="gpt-3.5-turbo",
        base_url=None,
        label="chatgpt",
        open_api_key=environ.get("OPENAI_API_KEY"),
    )
    GPT4 = LLMConfig(
        model="gpt-4",
        base_url=None,
        label="gpt4",
        open_api_key=environ.get("OPENAI_API_KEY"),
    )
    
    @classmethod
    def get_enum_by_model(cls, label_to_match: str):
        for item in cls:
            if item.value.label == label_to_match:
                return item
            
IO_DIR = "~/streamlit_conversations"