import boto3
import io
import pydicom
from PIL import Image
import streamlit as st
import sqlite3
from pandas.core.frame import DataFrame
import pandas as pd


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn


def instantiate_queries_table():
    try:
        conn = create_connection("queries.db")
        conn.execute(
            """
            create table queries (query_name varchar, query_contents varchar);
        """,
        )
        conn.commit()
        # always go for default index names when possible
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            ON queries(query_name);
        """,
        )
        conn.commit()

    except:
        pass


def sql_to_df(conn, query):
    """
    Pandas does this well, maybe just copy there's
    """
    results = conn.execute(query)

    cols = [column[0] for column in results.description]
    results_df = pd.DataFrame.from_records(
        data=results.fetchall(),
        columns=cols,
    )
    return results_df


def delete_component(conn, query: str, column_name: str, delete_statement: str):
    """
    Pandas does this well, maybe just copy there's
    """

    instantiate_queries_table()
    queries_df = sql_to_df(conn, query)
    st.dataframe(queries_df)
    query_to_delete = st.selectbox("Query to Delete", list(queries_df[column_name]))

    if st.button("Delete"):
        st.write(delete_statement)
        conn.execute(delete_statement)
        conn.commit()
        queries_df = sql_to_df(conn, query)
        st.dataframe(queries_df)


def get_image_direct_from_s3(bucket: str, key: str):
    """
    Given dicom_s3_details as retrieved from training collection
    Returns dicom object kept inmemory.
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(key)

    file_stream = io.BytesIO()
    obj.download_fileobj(file_stream)
    return file_stream


def get_s3_metadata(response_df: DataFrame) -> DataFrame:
    s3_metadata = pd.DataFrame(
        ml_dataset.find(
            {"_id": {"$in": list(response_df["id"])}},
            {"new_s3_info": 1},
        ),
    )
    s3_metadata["payload.s3_bucket"] = s3_metadata["new_s3_info"].apply(lambda x: x.get("PNG_256", {}).get("Bucket"))
    s3_metadata["payload.s3_key"] = s3_metadata["new_s3_info"].apply(lambda x: x.get("PNG_256", {}).get("Key"))

    new_response_df = pd.merge(response_df, s3_metadata, left_on="id", right_on="_id", how="inner")
    return new_response_df


def prep_display_content(response_df):  # make sure things stay in sync if there's an error loading the png
    """Retrieves the image for each instance_uuid at the same time as parsing the
    relevant metadata so that they remain in sync ready for display
    (image retrieval can fail in some cases)
    Args:
        response_df: Dataframe containing the Vector DB response
    """
    payload_columns = [col for col in response_df.columns.tolist() if "payload" in col]
    response_df = get_s3_metadata(response_df)
    metadata = response_df[payload_columns]
    pngs = []
    instance_uuids = []
    metadata_list = []
    with st.spinner("One second.."):
        for counter, (instance_uuid, bucket, key) in enumerate(
            zip(response_df["id"], response_df["payload.s3_bucket"], response_df["payload.s3_key"]),
        ):
            try:
                key = key.replace("256", "1024")  # tmp fix
                pngs.append(get_image_direct_from_s3(bucket, key))
                logger.info(f"{bucket}/{key}")
                instance_uuids.append(instance_uuid)
                metadata_list.append(metadata.iloc[counter].astype(str))
            except Exception as e:
                logger.debug(f"{e} :: {bucket}/{key}")
    return pngs, instance_uuids, metadata_list
