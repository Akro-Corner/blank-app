import streamlit as st
import pandas as pd
from supabase import create_client

if not "logged_user" in st.session_state:
    st.switch_page("streamlit_app")
    st.error("Session expired!")

#-------------------------

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

#-------------------------

def init_lcl_connect():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    return create_client(url, key)

sb = init_lcl_connect()

def retrieve_data():
    response = sb.table("todos").select("*").execute()
    return pd.DataFrame(response.data)

#-------------------------

st.header("DataSuite - " + st.session_state("logged_user"))
st.divider()

st.badge("Tiempo Real", color="green", icon="☁")
st.subheader("Pedidos Actuales.")


