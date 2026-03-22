import streamlit as st
import pandas as pd
from supabase import create_client
import supabase

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
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.badge("Actualizando...", color="blue", icon="☁")
st.subheader("Pedidos Actuales")

# 2. Fetch data from the "todos" table
# We use select("*") to get the ID, task_name, and is_completed status
response = supabase.table("todos").select("*").execute()
todos_data = response.data

if todos_data:
    for todo in todos_data:
        # Create a layout with two columns
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"**{todo['task_name']}**")
            
        with col2:
            # 3. This checkbox triggers the SQL Update
            # The 'key' must be unique, so we use the database ID
            is_done = st.checkbox("Done", value=todo["is_completed"], key=str(todo["id"]))
            
            # 4. Only send update to Supabase if the value actually changed
            if is_done != todo["is_completed"]:
                supabase.table("todos") \
                    .update({"is_completed": is_done}) \
                    .eq("id", todo["id"]) \
                    .execute()
                
                # Refresh the UI to show the new state
                st.rerun()
else:
    st.info("No tasks found in the 'todos' table.")