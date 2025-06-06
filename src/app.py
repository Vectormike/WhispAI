import streamlit as st
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks import CallbackManager

# page configuration
st.set_page_config(
    page_title="Llama Chatbot",
    page_icon="🦙",
    layout="wide"
)

# initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# initialize llm
llm = Ollama(
    model="llama3",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)


st.title("🦙 Llama 3 Chatbot 🦙")

# display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# user input
if prompt := st.chat_input("Send a message"):
    # display user message in chat message container
    st.chat_message("user").write(prompt)
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # display assistant response in chat message container
    with st.chat_message("assistant"):
        # query llm
        response = llm(prompt)
        # display response
        st.write(response)


