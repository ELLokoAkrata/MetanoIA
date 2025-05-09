"""
Módulo para la barra lateral de la aplicación.
"""
import streamlit as st
from src.models.config import AVAILABLE_MODELS

def render_sidebar(session_state, groq_client, logger):
    """
    Renderiza la barra lateral con opciones de configuración.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
        groq_client (GroqClient): Cliente de la API de Groq.
        logger (logging.Logger): Logger para registrar información.
        
    Returns:
        bool: True si se ha cambiado alguna configuración, False en caso contrario.
    """
    with st.sidebar:
        st.title("⚙️ Configuración")
        
        # Configuración de la API
        st.subheader("API")
        api_key = groq_client.api_key
        if not api_key:
            api_key = st.text_input("Groq API Key", type="password")
            if api_key:
                groq_client.set_api_key(api_key)
        
        # Selección de modelo
        st.subheader("Modelo")
        
        # Usar key para forzar la recreación del widget cuando cambia el modelo
        selected_model = st.selectbox(
            "Selecciona un modelo",
            options=list(AVAILABLE_MODELS.keys()),
            format_func=lambda x: AVAILABLE_MODELS[x],
            index=list(AVAILABLE_MODELS.keys()).index(session_state.context["model"]) 
                if session_state.context["model"] in AVAILABLE_MODELS else 0,
            key=f"model_select_{session_state.context['model']}"
        )
        
        # Parámetros de generación
        st.subheader("Parámetros")
        temperature = st.slider(
            "Temperatura", 
            min_value=0.0, 
            max_value=1.0, 
            value=session_state.context["temperature"],
            step=0.1,
            help="Controla la aleatoriedad de las respuestas. Valores más altos = más creatividad."
        )
        
        max_tokens = st.slider(
            "Máximo de tokens", 
            min_value=256, 
            max_value=4096, 
            value=session_state.context["max_tokens"],
            step=128,
            help="Número máximo de tokens en la respuesta."
        )
        
        # System prompt
        st.subheader("System Prompt")
        system_prompt = st.text_area(
            "Instrucciones para el asistente",
            value=session_state.context["system_prompt"],
            height=150
        )
        
        # Detectar cambios en la configuración
        config_changed = False
        
        # Actualizar contexto cuando cambian los valores
        if (selected_model != session_state.context["model"]):
            logger.info(f"Cambio de modelo: {session_state.context['model']} -> {selected_model}")
            session_state.context["model"] = selected_model
            config_changed = True
        
        if (temperature != session_state.context["temperature"] or
            max_tokens != session_state.context["max_tokens"] or
            system_prompt != session_state.context["system_prompt"]):
            
            logger.info(f"Cambio de parámetros: temperatura={temperature}, max_tokens={max_tokens}")
            session_state.context["temperature"] = temperature
            session_state.context["max_tokens"] = max_tokens
            session_state.context["system_prompt"] = system_prompt
            config_changed = True
        
        # Botón para limpiar la conversación
        if st.button("Limpiar conversación"):
            logger.info("Conversación limpiada")
            session_state.messages = []
            return True
        
        return config_changed
