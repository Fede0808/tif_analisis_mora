import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        try:
            valid_user = st.secrets["auth"]["username"]
            valid_pass = st.secrets["auth"]["password"]
        except KeyError:
            st.error("⚠️ Configuración de seguridad incompleta (faltan secrets).")
            return

        if st.session_state["username"] == valid_user and st.session_state["password"] == valid_pass:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Iniciar sesión", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Iniciar sesión", on_click=password_entered)
        st.error("😕 Usuario o contraseña incorrectos")
        return False
    
    else:
        # Password correct.
        return True
