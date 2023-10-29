import autogen
from nova_chat.constants import (
    get_url,
    AIIP,
    PORT,
)

config_list = [
    {
        "api_key": get_url(ip=AIIP, port=PORT)
    }
]

llm_config = {
    "request_timeout": 800,
    "config_list": config_list
}

assistant = autogen.AssistantAgent(
    "assistant",
    llm_config = llm_config
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config = {
        "work_dir": "coding"
    }
)

user_proxy.initiate_chat(
    assistant,
    message="write a python code to find even number"
)