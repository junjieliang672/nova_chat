import sys
import os
sys.path.append(os.getcwd())

from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from nova_chat.constants import RemoteLLM

llm = Ollama(base_url=RemoteLLM.LLAMA2.value.base_url, 
             model=RemoteLLM.LLAMA2.value.model, 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))

if __name__ == "__main__":
    llm("Tell me about the history of AI")