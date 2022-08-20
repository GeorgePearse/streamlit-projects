st.markdown("# Upload Data")
# https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
db_filename = st.selectbox('DB Filename', sqlite_dbs)
table_name = st.text_input('Table Name to Insert')
conn = create_connection(db_filename)
uploaded_file = st.file_uploader('Choose a file')
if uploaded_file is not None:
    #read csv
    try:
        df = pd.read_csv(uploaded_file)
        df.to_sql(name=table_name, con=conn)
        st.write('Data uploaded successfully. These are the first 5 rows.')
        st.dataframe(df.head(5))

    except Exception as e:
        st.write(e)