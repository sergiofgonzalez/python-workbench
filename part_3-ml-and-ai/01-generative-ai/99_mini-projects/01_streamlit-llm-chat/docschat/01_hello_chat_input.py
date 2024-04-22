"""Illustrates how to use st.chat_input"""
import streamlit as st

prompt = st.chat_input("Type something here...")
if prompt:
    st.write(f"You typed: {prompt!r}")