"""Illustrates how to use st.chat_message"""
import streamlit as st
import numpy as np

with st.chat_message("user"):
    st.write("Hello, 👋")

with st.chat_message("ai"):
    st.write("Hello, back! How can I help you today?")
    st.write("Here you are! A random bar chart:")
    st.bar_chart(np.random.randn(10, 3))

# no with
message_container = st.chat_message("ai")
message_container.write("Ask me anything!")
message_container.bar_chart(np.random.randn(10, 2))
