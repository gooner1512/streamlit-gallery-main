import pandas as pd
import streamlit as st
import pyodbc

class Database:
    def __init__(self):
        self.conn = self.init_connection()

    @staticmethod    
    @st.cache_resource
    def init_connection():
        return pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"]
        )
    def hash_connection(conn):
        # Return a hash of the connection string
        return hash(conn.getinfo(pyodbc.SQL_DRIVER_NAME))

      
    #@st.cache(hash_funcs={pyodbc.Connection: hash_connection},allow_output_mutation=True,ttl=3600)
    @st.cache_data(ttl=3600)
    def run_query(_conn, query):
        with _conn.cursor() as cur:
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
    
    #@st.cache(hash_funcs={pyodbc.Connection: hash_connection},allow_output_mutation=True,ttl=3600)
    @st.cache_data(ttl=3600)
    def run_query_multi_tables(_conn, query):
        with _conn.cursor() as cur:
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