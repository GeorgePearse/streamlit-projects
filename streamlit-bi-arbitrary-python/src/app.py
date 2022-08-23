import streamlit as st
from utils import create_connection

# make sure the db exists irrespective of where user comes from
create_connection("core.db")

with open("../README.md") as fh:
    long_description = fh.read()

# just paste most of your medium arcticle here
st.markdown(long_description)
