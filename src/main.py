import  json
import os
import streamlit as st
from groq import Groq

#streamlite page configuration
st.set_page_config(page_title="LLAMA-3.1 Chatbot"
                   ,page_icon="🦙",
                   layout="centered")

# when you go this code to other the path is different
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

#save this key to env
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

#UI design for streamlit app

#initialize the chat history as streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("LLAMA-3.1 Chatbot")
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# [{"role":"user","content":"What is Llama-3.1?"},
# {"role":"assistant","content":"LLM response"}]

user_input = st.chat_input("Ask a question about Llama-3.1")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    #send user's message to the LLM and get a response
    message = [
        {"role": "system", "content": "You are a helpful assistant."},  # Corrected this line
        *st.session_state.chat_history,
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=message,
    )
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)