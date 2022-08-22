# From https://gist.github.com/robwalton/d985ffd0b3f319919f3d79da7873d762

import json
import logging
import os

import pandas as pd

from mongo import MongoConnection
from utils import prep_display_content

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

vector_db_host = os.environ.get("VECTOR_DB_HOST")
ml_dataset = MongoConnection(
    user=os.environ.get("ML_MONGO_USER"),
    password=os.environ.get("ML_MONGO_PASSWORD"),
    host=os.environ.get("ML_MONGO_HOST"),
).get_collection("ml-cxr-datalake")


st.markdown("# Run and Save Queries")

collections = [
    record["name"] for record in requests.get(f"{vector_db_host}/collections").json()["result"]["collections"]
]

collection_name = st.selectbox("Collection", collections)

query_name = st.text_input("Query Name (For Saving)")
query_results = "./pages/results/"
saved_queries = "./pages/saved_queries/"
examples = os.listdir(saved_queries)
choice = st.selectbox("Examples", examples)

with open(f"{saved_queries}/{choice}") as f:
    selected_query = json.load(f)
    logger.info(f"{selected_query} worked")

col1, col2 = st.columns(2)
with col1:
    # load example
    st.write(selected_query)
with col2:
    # edit as wanted
    string_query = st.text_area(label="query")

request = f"collections/{collection_name}/points/recommend"
url = f"{vector_db_host}/{request}"

save_query = st.checkbox("Save Query")
if st.button("Run Query"):
    # if outside of this button it will execute on initial load
    # have no string content, and error.
    data = json.loads(string_query)

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

        response_df = pd.json_normalize(response["result"])
        st.dataframe(response_df)

        pngs, instance_uuids, metadata_list = prep_display_content(
            ml_dataset,
            response_df,
        )
        logger.info(len(pngs))
        skipping_elements = range(len(pngs) // 2)
        logger.info(list(skipping_elements))
        for counter in skipping_elements:
            cols = st.columns(4)
            cols[0].image(pngs[counter * 2], caption=instance_uuids[counter * 2])
            cols[1].dataframe(data=metadata_list[counter * 2])
            cols[2].image(
                pngs[(counter * 2) + 1],
                caption=instance_uuids[(counter * 2) + 1],
            )
            cols[3].dataframe(data=metadata_list[(counter * 2) + 1])

        if save_query:

            with open(
                f"./{saved_queries}/{query_name}.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            response_df.to_csv(f"./{query_results}/{query_name}.csv")

        st.download_button(
            label="Download data as CSV",
            data=response_df.to_csv().encode("utf-8"),
            file_name=f"{query_name}.csv",
        )
    except Exception as e:
        st.write(f"Please complete the form \n Exception = {e}")
