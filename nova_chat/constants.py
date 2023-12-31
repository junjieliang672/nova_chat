from enum import Enum
from typing import Optional
from pydantic import BaseModel
import os
from os import environ, path
from functools import partial


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
    MISTRAL = LLMConfig(
        model="mistral:7b-instruct",
        base_url=get_url(),
        label="mistral"
    )
    LLAMA2_13B = LLMConfig(
        model="llama2:13b",
        base_url=get_url(),
        label="ollama-llama2-13b",
    )
    CODELLAMA = LLMConfig(
        model="codellama",
        base_url=get_url(),
        label="ollama-codellama-7b",
    )
    STARCODER = LLMConfig(
        model="starcoder",
        base_url=get_url(),
        label="starcoder",
    )
    ORCA2 = LLMConfig(
        model="orca2",
        base_url=get_url(),
        label="orca2",
    )
    
    CHATGPT_16K = LLMConfig(
        model="gpt-3.5-turbo-16k",
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
            
IO_DIR = path.join(os.getenv("HOME"), "streamlit_conversations")
APP_USERS = ["Jetfeet", "Junhead"]