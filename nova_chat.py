import sys
import os
from icecream import ic
sys.path.append(os.getcwd())

from nova_chat.chatbots import build_streamlit_demo as chatbot_demo
    
if __name__ == "__main__":
    chatbot_demo()