import streamlit as st

st.text_input("Your name", key="name")
print(st.session_state.name)
