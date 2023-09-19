import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40]
})

option = st.selectbox(
    "What number do you like best?",
    df["first column"]
)

st.write("You selected: ", option)
