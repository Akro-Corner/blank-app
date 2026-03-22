import streamlit as st
import pandas as pd
from supabase import create_client

st.markdown(
    """
    <style>
        /* This hides the sidebar itself */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* This hides the ' > ' arrow button that lets users open it */
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if not "logged_user" in st.session_state:
    st.switch_page("streamlit_app.py")
    st.error("Session expired!")

#-------------------------

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
todos = 1

#-------------------------

def init_lcl_connect():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    return create_client(url, key)

sb = init_lcl_connect()

@st.cache_data(ttl=600)
def retrieve_data():
    response = sb.table("todos").select("*").execute()
    todos = response.data
    return pd.DataFrame(response.data)
    

#-------------------------

st.header("DataSuite - " + st.session_state["logged_user"])
st.divider()

st.badge("Tiempo Real", color="green", icon="☁")
st.subheader("Pedidos Actuales.")

df = retrieve_data()



for todo in todos:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(todo["task_name"])
    
    with col2:
        # 2. When this checkbox is clicked, it triggers an UPDATE
        checked = st.checkbox("Done", value=todo["is_completed"], key=todo["id"])
        
        if checked != todo["is_completed"]:
            supabase.table("todos") \
                .update({"is_completed": checked}) \
                .eq("id", todo["id"]) \
                .execute()
            st.rerun()

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = df.set_index("created_at")

    st.subheader("Data Overview")
    st.write(df.head())

    st.subheader("Visualized Data")
    st.line_chart(df[["value_column_name"]]) 
else:
    st.info("No data found in Supabase.")


