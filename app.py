"""
MetanoIA: Un chatbot modular con múltiples modelos de lenguaje.

Esta aplicación permite interactuar con diferentes modelos de lenguaje a través 
de una interfaz de chat moderna y configurable, manteniendo el contexto de la 
conversación al cambiar entre modelos.
"""
import streamlit as st

# Importar módulos propios
from src.utils.logger import setup_logger
from src.utils.styles import apply_fresh_tech_theme
from src.utils.session_state import initialize_session_state
from src.models.config import AVAILABLE_MODELS
from src.api.groq_client import GroqClient
from src.components.sidebar import render_sidebar
from src.components.chat import display_chat_history, handle_user_input, display_agentic_context

# Configuración de la página
st.set_page_config(
    page_title="MetanoIA", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

def main():
    """Función principal de la aplicación."""
    # Configurar el logger
    logger = setup_logger("MetanoIA")
    
    # Aplicar el tema personalizado
    apply_fresh_tech_theme()
    
    # Inicializar el estado de la sesión
    session_state = initialize_session_state()
    
    # Inicializar el cliente de Groq
    groq_client = GroqClient(logger=logger)
    
    # Título principal
    st.title("🤖 MetanoIA")
    st.markdown("Chat bot modular usando Streamlit y la API de Groq")
    
    # Renderizar la barra lateral
    config_changed = render_sidebar(session_state, groq_client, logger)
    
    # Si la configuración cambió, recargar la página
    if config_changed:
        st.rerun()
    
    # Contenedor principal del chat
    chat_container = st.container()
    
    # Mostrar mensajes anteriores
    with chat_container:
        display_chat_history(session_state, AVAILABLE_MODELS)
    
    # Entrada de usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        handle_user_input(prompt, session_state, groq_client, logger)

if __name__ == "__main__":
    main()
