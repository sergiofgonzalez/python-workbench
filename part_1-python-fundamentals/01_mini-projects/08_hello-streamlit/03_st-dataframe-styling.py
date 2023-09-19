"""
Create a Streamlit app that shows a table backed by a
Pandas dataframe whose content is some random data generated
using numpy
"""

import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=(f'col {i + 1}' for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
