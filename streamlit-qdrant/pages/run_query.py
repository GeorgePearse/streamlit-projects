# From https://gist.github.com/robwalton/d985ffd0b3f319919f3d79da7873d762

import json
import pandas as pd
from PIL import Image
from typing import List
import os
import json
from mongo import MongoConnection
from utils import prep_display_content, get_image_direct_from_s3, get_s3_metadata, sql_to_df, instantiate_queries_table

import logging

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger("pythonConfig")
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)
import requests
import streamlit as st

from pymongo import MongoClient
from pandas.core.frame import DataFrame
from utils import create_connection, instantiate_queries_table, get_image_direct_from_s3

vector_db_host = os.environ.get("VECTOR_DB_HOST")
ml_dataset = MongoConnection(
    user=os.environ.get("ML_MONGO_USER"),
    password=os.environ.get("ML_MONGO_PASSWORD"),
    host=os.environ.get("ML_MONGO_HOST"),
).get_collection("ml-cxr-datalake")


st.markdown("# Run Query")
query_name = st.text_input("Query Name")

# where you're going to store your QDrant Queris
queries_conn = create_connection("queries.db")

save_query = st.checkbox("Save Query")
run_query = st.button("Run Query")

instantiate_queries_table()
queries_df = sql_to_df(queries_conn, "select * from queries")

try:
    selected_query = st.selectbox("Query to Execute", list(queries_df["query_name"]))
    selected_mask = queries_df["query_name"] == selected_query
    selected_query = queries_df[selected_mask]["query_contents"].iloc[0]
except Exception as e:
    # fall back to get started
    selected_query = {
        "positive": ["c74fead7-78db-449a-abd7-8bab4b459e64"],
        "negative": [],
        "top": 10,
        "with_payload": True,
        "filter": {"must_not": [{"is_empty": {"key": "classes"}}]},
    }


col1, col2 = st.columns(2)
with col1:
    # load example
    st.write(selected_query)
with col2:
    # edit as wanted
    data = json.loads(st.text_area(label="query"))
    # in case it doesn't already exist


collection_name = "cxr-metadata-cosine"
request = f"collections/{collection_name}/points/recommend"
url = f"{vector_db_host}/{request}"

try:
    response = requests.post(url, json=data).json()

    code = f"""
data = {data}
url = '{url}'
response = requests.post(url, json=data).json()
"""
    st.code(code, language="python")

    with st.expander("JSON Response"):
        st.json(response)
    try:
        # for scroll endpoint
        response_df = pd.json_normalize(response["result"]["points"])
    except:
        # for recommend endpoint
        response_df = pd.json_normalize(response["result"])

    st.dataframe(response_df)

    pngs, instance_uuids, metadata_list = prep_display_content(response_df)
    logger.info(len(pngs))
    skipping_elements = range(len(pngs) // 2)
    logger.info(list(skipping_elements))
    for counter in skipping_elements:
        cols = st.columns(4)
        cols[0].image(pngs[counter * 2], caption=instance_uuids[counter * 2])
        cols[1].dataframe(data=metadata_list[counter * 2])
        cols[2].image(pngs[(counter * 2) + 1], caption=instance_uuids[(counter * 2) + 1])
        cols[3].dataframe(data=metadata_list[(counter * 2) + 1])

    st.download_button(
        label="Download data as CSV",
        data=response_df.to_csv().encode("utf-8"),
        file_name="nearest_neighbours.csv",
    )
except Exception as e:
    st.write(f"Please complete the form \n Exception = {e}")
