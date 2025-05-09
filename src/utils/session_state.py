"""
Módulo para la gestión del estado de la sesión.
"""
import streamlit as st

def initialize_session_state():
    """
    Inicializa el estado de la sesión si no existe.
    
    Returns:
        SessionState: Estado de la sesión de Streamlit.
    """
    # Inicialización de variables de sesión para mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Inicialización de variables de sesión para el contexto
    if "context" not in st.session_state:
        st.session_state.context = {
            "model": "deepseek-r1-distill-llama-70b",
            "temperature": 0.7,
            "max_tokens": 1024,
            "system_prompt": "Eres un asistente virtual amigable y útil."
        }
    
    return st.session_state
