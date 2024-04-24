"""Streamlit application of bot that echoes user's input"""

import random
import time

import streamlit as st


def response_generator():
    """
    Returns a generator function for random response from the list of canned
    response.
    """
    response = random.choice(
        [
            "I'm sorry, I didn't understand that. Can you elaborate?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help with anything?",
            "The result is pi. Just kidding! 😆",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.02)


st.title("Canned Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type something here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display bot response
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())

    st.session_state.messages.append({"role": "assistant", "content": response})
