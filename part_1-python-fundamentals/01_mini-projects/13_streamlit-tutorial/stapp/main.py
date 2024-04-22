"""Streamlit tutorial"""

import numpy as np
import pandas as pd
import streamlit as st

st.write("## Hello, world!")
name = st.text_input("What's your name?")
st.write(f"Hello, {name}!")
print(f"{name=}")
is_clicked = st.button("Click me!")
print(f"{is_clicked=}")

# working with data
data = pd.read_csv("data/people.csv")
st.write(data)

# charts
chart_data = pd.DataFrame(data=np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)
st.line_chart(chart_data)

# Basic integration with other sites/apps
st.write("## Working with link buttons for integration")
title = st.text_input("Enter the title")
st.link_button(
    "Search in IMDB",
    f"https://www.imdb.com/find/?q={title}",
)
