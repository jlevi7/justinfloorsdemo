import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(page_title="JustinFloors Demo", layout="wide")
st.title("JustinFloors Demo Dashboard")

@st.cache_data(ttl=60)
def load_jobs():
    conn = mysql.connector.connect(
        host=st.secrets["db"]["host"],
        port=int(st.secrets["db"]["port"]),
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["database"],
    )
    query = """
    SELECT 
      j.job_id,
      c.full_name AS customer,
      CONCAT(j.address_line1, ', ', j.city) AS address,
      s.status_name AS status,
      j.install_start_date,
      j.installer_name
    FROM jobs j
    JOIN customers c ON c.customer_id = j.customer_id
    JOIN statuses s ON s.status_id = j.status_id
    ORDER BY s.sort_order, j.install_start_date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    df = load_jobs()
    st.subheader("Jobs")
    st.dataframe(df, use_container_width=True)

    st.subheader("Jobs by Status")
    st.dataframe(df["status"].value_counts().reset_index().rename(columns={"index": "status", "status": "count"}))

except Exception as e:
    st.error("Database connection failed.")
    st.code(str(e))
    st.info("Double-check Streamlit secrets and make sure your MySQL database is reachable from the internet.")
