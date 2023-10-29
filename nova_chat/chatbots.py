from nova_chat.constants import RemoteLLM
from nova_chat.llm_client import LLMFactory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
from icecream import ic

def getConversation(memory, model, st=None):
    chat = LLMFactory.getChat(model, st)
    
    # Prompt 
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    return LLMChain(
        llm=chat,
        prompt=prompt,
        verbose=False,
        memory=memory
    )
    

def form_prompt_history(messages, memory):
    input, output = None, None
    for message in messages:
        if message["role"] == "user":
            input = message["content"]
        else:
            output = message["content"]
        
        if input and output:
            memory.save_context({"input": input}, {"output": output})
            input, output = None, None
            

def clear_chat_history():
    st.session_state.messages = []
    

def select_model():
    return st.selectbox(
        "What model do you want to use?",
        (x.value.label for x in RemoteLLM),
    )


def build_streamlit_demo():
    with st.sidebar:
        st.button('Clear chat history', on_click=clear_chat_history)
        v = select_model()
        model = RemoteLLM.get_enum_by_model(v)
    
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    chat = getConversation(memory, model, st)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.container():
        st.write("------------- Chat history -------------")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    if prompt := st.chat_input("What's up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        form_prompt_history(st.session_state.messages, memory)
        res = chat({"question":prompt})
        st.session_state.messages.append({"role": "assistant", "content": res["text"]})