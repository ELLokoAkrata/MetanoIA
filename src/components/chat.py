"""
Módulo para el componente de chat de la aplicación.
"""
import streamlit as st
from src.models.config import get_model_display_name, get_context_limit

def display_chat_history(session_state, models):
    """
    Muestra el historial de mensajes del chat.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
        models (dict): Diccionario de modelos disponibles.
    """
    for i, msg in enumerate(session_state.messages):
        with st.chat_message(msg["role"]):
            # Si es un mensaje del asistente y tiene información del modelo usado, mostrarla
            if msg["role"] == "assistant" and "model_used" in msg:
                model_name = get_model_display_name(msg["model_used"])
                st.caption(f"Generado por: {model_name}")
            
            # Mostrar el contenido del mensaje
            st.markdown(msg["content"])

def prepare_api_messages(session_state, current_model, logger):
    """
    Prepara los mensajes para enviar a la API, filtrando campos personalizados
    y limitando el contexto según el modelo.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
        current_model (str): ID del modelo actual.
        logger (logging.Logger): Logger para registrar información.
        
    Returns:
        list: Lista de mensajes preparados para la API.
    """
    # Preparar mensajes para la API (filtrando campos personalizados y limitando el contexto)
    api_messages = [
        {"role": "system", "content": session_state.context["system_prompt"]}
    ]
    
    # Obtener el número máximo de mensajes a incluir según el modelo
    max_context_messages = get_context_limit(current_model)
    
    # Registrar el límite de contexto aplicado
    logger.info(f"Limitando contexto a {max_context_messages} mensajes para el modelo {current_model}")
    
    # Añadir mensajes del historial filtrando campos personalizados y limitando la cantidad
    # Tomamos solo los mensajes más recientes para no exceder los límites
    recent_messages = session_state.messages[-max_context_messages:] if len(session_state.messages) > max_context_messages else session_state.messages
    
    for msg in recent_messages:
        if msg["role"] in ["user", "assistant"]:
            # Solo incluir campos estándar (role y content)
            api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    return api_messages

def handle_user_input(prompt, session_state, groq_client, logger):
    """
    Maneja la entrada del usuario y genera una respuesta.
    
    Args:
        prompt (str): Mensaje del usuario.
        session_state (SessionState): Estado de la sesión de Streamlit.
        groq_client (GroqClient): Cliente de la API de Groq.
        logger (logging.Logger): Logger para registrar información.
    """
    # Verificar que tenemos una API key
    if not groq_client.is_configured():
        st.error("Por favor, ingresa tu API key de Groq en la barra lateral.")
        return
    
    # Obtener el modelo actual directamente del contexto
    current_model = session_state.context["model"]
    logger.info(f"Usando modelo seleccionado: {current_model} ({get_model_display_name(current_model)})")
    
    # Agregar mensaje del usuario al historial
    session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar mensajes para la API
    api_messages = prepare_api_messages(session_state, current_model, logger)
    
    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        # Mostrar qué modelo se está usando
        model_info = st.empty()
        model_info.info(f"Generando respuesta con {get_model_display_name(current_model)}...")
        
        # Contenedor para la respuesta
        response_container = st.empty()
        
        # Función de callback para actualizar la respuesta en tiempo real
        def update_response(text):
            # Eliminar el mensaje de información
            model_info.empty()
            # Actualizar el contenido de la respuesta
            response_container.markdown(text)
        
        # Generar respuesta
        full_response = groq_client.generate_streaming_response(
            model=current_model,
            messages=api_messages,
            temperature=session_state.context["temperature"],
            max_tokens=session_state.context["max_tokens"],
            callback=update_response
        )
        
        # Mostrar la respuesta final (por si acaso el callback no se ejecutó correctamente)
        model_info.empty()
        response_container.markdown(full_response)
    
    # Agregar respuesta al historial con información del modelo usado
    session_state.messages.append({
        "role": "assistant", 
        "content": full_response, 
        "model_used": current_model
    })
