import pandas as pd
import streamlit as st
import pyodbc
import time

class Database:
    def __init__(self, max_retries=3, retry_interval=5):
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    @staticmethod    
    @st.cache_resource()
    def init_connection():
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server}"
            + ";SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"]
            + ";Trust Server Certificate=true"
            + ";ENCRYPT=No"
        )
        return conn
    
    
    @st.cache_data(ttl=3600)
    def run_query(_self, query):
        retries = 0
        while retries < _self.max_retries:
            try:
                with _self.init_connection().cursor() as cur:
                    cur.execute(query)
                    # Fetch the rows
                    rows = cur.fetchall()

                    # Get the column names from the cursor description
                    column_names = [column[0] for column in cur.description]

                    # Separate the columns into separate lists
                    columns = []
                    for i in range(len(column_names)):
                        column = [row[i] for row in rows]
                        columns.append(column)

                    # Create the DataFrame
                    df = pd.DataFrame({column_names[i]: columns[i] for i in range(len(column_names))})
                    
                    return df
            except pyodbc.OperationalError as e:
                if 'Communication link failure' in str(e):
                    retries += 1
                    st.cache_resource.clear()
                    time.sleep(_self.retry_interval)
                    
                else:
                    raise e
        # If we have reached max_retries, raise the error
        raise pyodbc.OperationalError('Failed to connect to the database server after {} retries.'.format(_self.max_retries))
        
    
    @st.cache_data(ttl=3600)
    def run_query_multi_tables(_self, query):
        retries = 0
        while retries < _self.max_retries:
            try:
                with _self.init_connection().cursor() as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    columns = [column[0] for column in cur.description]
                    df_list = []
                    df_list.append(pd.DataFrame.from_records(rows, columns=columns))
                    
                    while (cur.nextset()): 
                        rows = cur.fetchall()
                        columns = [column[0] for column in cur.description]
                        df_list.append(pd.DataFrame.from_records(rows, columns=columns))

                    return df_list
            except pyodbc.OperationalError as e:
                if 'Communication link failure' in str(e):
                    retries += 1
                    st.cache_resource.clear()
                    time.sleep(_self.retry_interval)
                    
                else:
                    raise e
        # If we have reached max_retries, raise the error
        raise pyodbc.OperationalError('Failed to connect to the database server after {} retries.'.format(_self.max_retries))
        
    # def hash_connection(conn):
    #     # Return a hash of the connection string
    #     return hash(conn.getinfo(pyodbc.SQL_DRIVER_NAME))

      
    #@st.cache(hash_funcs={pyodbc.Connection: hash_connection},allow_output_mutation=True,ttl=3600)