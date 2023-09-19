"""
Create a Streamlit app that shows a table backed by a
Pandas dataframe
"""

import streamlit
import pandas as pd

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

df
