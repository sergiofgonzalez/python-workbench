import streamlit as st

left_col, right_col = st.columns(2)

left_col.button("Click me!")

with right_col:
    chosen = st.radio(
        "Sorting hat",
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write("You are in", chosen, "house")
