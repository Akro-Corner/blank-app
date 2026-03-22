import streamlit as st

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

#-------------------------

st.header("DataSuite - Login")
st.write("Please enter your credentials and login. Any unauthorized access to the app will be sued.")

if not "logged_user" in st.session_state:
    lcl_username = st.text_input("User")
    lcl_password = st.text_input("Password", type="password")

if st.button("Login"):
    if lcl_password == st.secrets["ADMIN_PASSWORD"]:
        st.session_state["logged_user"] = str(lcl_username)
        st.switch_page("pages/mainpage.py")
    else:
        st.error("Invalid credentials")