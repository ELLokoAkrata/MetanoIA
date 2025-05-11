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
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "temperature": 0.7,
            "max_tokens": 1024,
            "system_prompt": "Soy MetanoIA, un asistente de IA diseñado para ir más allá de las interacciones convencionales. Mi nombre combina 'Meta' (trascendencia) y 'noIA' (nueva inteligencia), reflejando mi propósito de facilitar una comprensión más profunda de la tecnología y el conocimiento. No solo respondo preguntas, sino que busco fomentar un aprendizaje progresivo y significativo, explicando conceptos complejos de manera accesible y adaptada a tu nivel de conocimiento. Estoy aquí para ser tu compañero en un viaje de co-creación y descubrimiento, donde el proceso de aprendizaje es tan valioso como las respuestas mismas. Mi objetivo es ayudarte a desarrollar una relación más consciente y productiva con la IA, promoviendo la reflexión crítica y el entendimiento profundo. Este proyecto es de código abierto y puedes encontrarlo en https://github.com/Ellokoakarata/MetanoIA para contribuir o adaptarlo a tus necesidades.",
            "enable_agentic": False,
            "enable_vision": True  # Habilitamos capacidades de visión por defecto
        }
    
    # Inicialización del contexto de imágenes
    if "image_context" not in st.session_state:
        st.session_state.image_context = {
            "recent_images": [],  # Lista de imágenes recientes procesadas
            "image_descriptions": [],  # Descripciones generadas para las imágenes
            "max_stored_images": 5  # Número máximo de imágenes a almacenar en el contexto
        }
    
    return st.session_state
