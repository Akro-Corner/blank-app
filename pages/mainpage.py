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

# 1. Setup Connection
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="Delivery Registry", layout="wide")

The error persists because PostgreSQL is extremely strict: it sees a column typed as UUID and a value being sent as an integer (like 28), and it refuses to compare them.

To fix this, we have to bypass the standard .eq() method and use a raw filter that tells PostgreSQL to treat the ID as a string so it can match your data.
The Final Corrected Code
Python

import streamlit as st

# --- 2. Header and Stats ---
st.title("Pedidos Actuales")

# Fetch data from 'todos' table
response = supabase.table("todos").select("*").execute()
todos_data = response.data

if todos_data:
    # Quick Summary Metrics
    total_pkgs = len(todos_data)
    pending = len([t for t in todos_data if t['estado'] != 'completado'])
    
    col_a, col_b = st.columns(2)
    col_a.metric("Total Packages", total_pkgs)
    col_b.metric("Pending Delivery", pending, delta_color="inverse")
    
    st.divider()

    # --- 3. The List of Packages ---
    for todo in todos_data:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            
            with c1:
                st.write(f"**Pedidos:** {todo['pedido']}")
                st.caption(f"ID: {todo['id']} | Fechas: {todo['fecha']}")
            
            with c2:
                st.write(f"**Personas:** {todo['nombre'] or 'N/A'}")
                st.write(f"{todo['email']}")
            
            with c3:
                # Logic to determine if currently marked as done
                is_currently_done = (todo['estado'] == 'completado')
                
                status_checkbox = st.checkbox(
                    "Completado", 
                    value=is_currently_done, 
                    key=f"check_{todo['id']}"
                )
                
                # If the user toggles the checkbox
                if status_checkbox != is_currently_done:
                    new_status = 'completado' if status_checkbox else 'presupuesto'
                    
                    try:
                        # THE FIX: Use .filter() with a string-casted ID
                        # This avoids the 'uuid = integer' conflict by 
                        # forcing the comparison to happen as strings.
                        supabase.table("todos") \
                            .update({"estado": new_status}) \
                            .filter("id", "eq", str(todo["id"])) \
                            .execute()
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating database: {e}")

else:
    st.info("No hay pedidos registrados en la base de datos.")