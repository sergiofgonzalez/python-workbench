"""
Create a Streamlit app that shows a table backed by a
Pandas dataframe
"""

import streamlit as st
import pandas as pd


st.write("Here's your first attempt at using data to create a table:")
df = pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40]
})

st.write(df)
