import boto3
import io
import streamlit as st
from pandas.core.frame import DataFrame
import pandas as pd
import logging


def get_json_formats_select_box():
    json_formats = ["split", "records", "index", "columns", "values", "table"]
    return st.selectbox("Json Format", json_formats)


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


def get_s3_metadata(ml_dataset, response_df: DataFrame) -> DataFrame:
    s3_metadata = pd.DataFrame(
        ml_dataset.find(
            {"_id": {"$in": list(response_df["id"])}},
            {"new_s3_info": 1},
        ),
    )
    s3_metadata["payload.s3_bucket"] = s3_metadata["new_s3_info"].apply(
        lambda x: x.get("PNG_256", {}).get("Bucket"),
    )
    s3_metadata["payload.s3_key"] = s3_metadata["new_s3_info"].apply(
        lambda x: x.get("PNG_256", {}).get("Key"),
    )

    new_response_df = pd.merge(
        response_df,
        s3_metadata,
        left_on="id",
        right_on="_id",
        how="inner",
    )
    return new_response_df


# TODO: This method of passing the mongo collection through is a mess and
# shouldn't be needed, it's only needed for the s3 details at the minute
def prep_display_content(
    ml_dataset,
    response_df,
):  # make sure things stay in sync if there's an error loading the png
    """Retrieves the image for each instance_uuid at the same time as parsing the
    relevant metadata so that they remain in sync ready for display
    (image retrieval can fail in some cases)
    Args:
        response_df: Dataframe containing the Vector DB response
    """
    payload_columns = [col for col in response_df.columns.tolist() if "payload" in col]
    response_df = get_s3_metadata(ml_dataset, response_df)
    metadata = response_df[payload_columns]
    pngs = []
    instance_uuids = []
    metadata_list = []
    with st.spinner("One second.."):
        for counter, (instance_uuid, bucket, key) in enumerate(
            zip(
                response_df["id"],
                response_df["payload.s3_bucket"],
                response_df["payload.s3_key"],
            ),
        ):
            try:
                key = key.replace("256", "1024")  # tmp fix
                pngs.append(get_image_direct_from_s3(bucket, key))
                logging.info(f"{bucket}/{key}")
                instance_uuids.append(instance_uuid)
                metadata_list.append(metadata.iloc[counter].astype(str))
            except Exception as e:
                logging.debug(f"{e} :: {bucket}/{key}")
    return pngs, instance_uuids, metadata_list
