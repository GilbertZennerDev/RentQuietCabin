import streamlit as st
import datetime

# Single date picker
date = st.date_input("Pick a date", datetime.date.today())
st.write("You selected:", date)

# Range of dates
date_range = st.date_input("Pick an halfhour range", [])
st.write("You selected range:", date_range)

items = ["Apples", "Bananas", "Cherries"]

st.write("### Clickable List")
for item in items:
    if st.button(item): on_click(item)
