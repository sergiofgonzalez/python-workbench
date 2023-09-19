"""
Create a Streamlit app that shows a table backed by a
Pandas dataframe whose content is some random data generated
using numpy
"""

import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

st.line_chart(chart_data)
