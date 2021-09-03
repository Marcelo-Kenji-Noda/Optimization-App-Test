import streamlit as st
from gsheetsdb import connect
from ortools.linear_solver import pywraplp

st.header("Hello World")
# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = "https://docs.google.com/spreadsheets/d/1E44kPwE84dW-hgSGCowRnj9rx2mZdm1HyiygtJ35ORU/edit?usp=sharing"
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a {row.cost}")

