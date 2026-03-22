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

# 2. Header and Stats
st.title("Pedidos Actuales")

# Fetch data from 'todos' table
response = supabase.table("todos").select("*").execute()
todos_data = response.data

if todos_data:
    # Quick Summary Metrics
    total_pkgs = len(todos_data)
    # Using 'completado' as the source of truth for logic
    pending = len([t for t in todos_data if t['estado'] != 'completado'])
    
    col_a, col_b = st.columns(2)
    col_a.metric("Total Packages", total_pkgs)
    col_b.metric("Pending Delivery", pending, delta_color="inverse")
    
    st.divider()

    # 3. The List of Packages
    for todo in todos_data:
        # Create a visual card for each package
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            
            with c1:
                st.write(f"**Pedidos:** {todo['pedido']}")
                st.caption(f"ID: {todo['id']} | Fechas: {todo['fecha']}")
            
            with c2:
                st.write(f"**Personas:** {todo['nombre'] or 'N/A'}")
                st.write(f"{todo['email']}")
            
            with c3:
                # Checkbox logic
                is_checked = (todo['estado'] == 'completado')
                
                status_checkbox = st.checkbox(
                    "Completado", 
                    value=is_checked, 
                    key=f"check_{todo['id']}"
                )
                
                # If the checkbox state differs from the database state
                if status_checkbox != is_checked:
                    # Determine new string based on checkbox
                    new_val = 'completado' if status_checkbox else 'presupuesto'
                    
                    # FIX: Explicitly cast todo["id"] to int to prevent the 'operator does not exist' error
                    try:
                        supabase.table("todos") \
                            .update({"estado": new_val}) \
                            .eq("id", int(todo["id"])) \
                            .execute()
                        
                        # Refresh the UI to show updated metrics
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating database: {e}")

else:
    st.info("No hay pedidos registrados en la base de datos.")