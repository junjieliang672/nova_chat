import datetime
import os
from nova_chat.constants import IO_DIR, RemoteLLM
from nova_chat.llm_client import LLMFactory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
from icecream import ic
import pandas as pd
from nova_chat.io import (
    memory_to_dict,
    save_message,
    load_message,
)

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
    """Build up the prompt memory from the session state messages."""
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
    
def build_sidebar():
    with st.sidebar:
        st.button('Clear chat history', on_click=clear_chat_history)
        v = select_model()
        model = RemoteLLM.get_enum_by_model(v)
        st.write("--")
    return model


def build_streamlit_demo():
    
    model = build_sidebar()
    memory = ConversationBufferWindowMemory(k=30, memory_key="chat_history", return_messages=True)
    chat = getConversation(memory,model, st)
    
    with st.sidebar:
        filename = st.text_input("Save conversation history to file","test.json")
        if st.button("Save conversation history",type="primary"):
            if st.session_state.messages:
                save_message(filename, st.session_state.messages)
                st.success("Done!")
            else:
                st.error("Empty session state!")
            
        with st.expander("List saved conversations:"):
            if not os.path.exists(IO_DIR):
                os.makedirs(IO_DIR)
                
            files = os.listdir(IO_DIR)
                
            file_modified_time = [
                datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(str(IO_DIR), str(file)))).isoformat() for file
                in files
            ]
            file_sizes = [
                format(os.path.getsize(os.path.join(IO_DIR, file)) / (1024 * 1024), f".2f") for
                file in files]
            files_with_time = pd.DataFrame(data=[files, file_modified_time, file_sizes],
                index=['Model', 'Last modified', 'Size in MB']).T
            st.dataframe(files_with_time)
            
            file = st.selectbox("Select a memory file to load", files)
            if st.button("Load conversations",type="primary"):
                messages = load_message(file)
                st.session_state.messages = []
                for message in messages:
                    st.session_state.messages.append({"role": "user", "content": message["input"]})
                    st.session_state.messages.append({"role": "assistant", "content": message["output"]})
                st.success("Loaded!")
                st.write(st.session_state.messages)
                    
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