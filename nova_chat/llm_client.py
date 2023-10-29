from langchain.llms import Ollama
from langchain.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from nova_chat.constants import RemoteLLM
from langchain.callbacks.base import BaseCallbackHandler

class LLMFactory:
    @staticmethod
    def getLLM(llm: RemoteLLM, st=None):
        if st:  # provide streamlit to set proper output streaming
            return Ollama(
                base_url=llm.value.base_url, 
                model=llm.value.model, 
                callback_manager = CallbackManager([StreamHandler(st)])
            )
        else:
            return Ollama(
                base_url=llm.value.base_url, 
                model=llm.value.model, 
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            )
    
    @staticmethod
    def getChat(llm: RemoteLLM, st = None):
        if st:  # provide streamlit to set proper output streaming
            return ChatOllama(
                base_url=llm.value.base_url, 
                model=llm.value.model, 
                callback_manager = CallbackManager([StreamHandler(st)])
            )
        else:
            return ChatOllama(
                base_url=llm.value.base_url, 
                model=llm.value.model, 
                callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            )
        

class StreamHandler(BaseCallbackHandler):
    """Stream printing handler."""
    def __init__(self, st, initial_text=""):
        self.st = st
        self.text=initial_text
        with st.chat_message("assistant"):
            self.message_placeholder = st.empty()
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token
        try:
            self.message_placeholder.markdown(self.text)
        except:
            self.message_placeholder.write(self.text)
