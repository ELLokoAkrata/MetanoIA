"""
Módulo para el componente de chat de la aplicación.
"""
import streamlit as st
import os
from src.models.config import get_model_display_name, get_context_limit, get_model
from src.utils.agentic_tools_manager import AgenticToolsManager
from src.components.audio import display_audio_input
from src.api.audio_transcription import AudioTranscriber

def display_chat_history(session_state, models):
    """
    Muestra el historial de mensajes del chat.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
        models (dict): Diccionario de modelos disponibles.
    """
    for i, msg in enumerate(session_state.messages):
        # Determinar el rol del mensaje (compatibilidad con formatos antiguos y nuevos)
        if "role" in msg:
            role = msg["role"]
        elif "is_user" in msg:
            role = "user" if msg["is_user"] else "assistant"
        else:
            # Si no se puede determinar el rol, usar un valor predeterminado
            role = "assistant"
            
        with st.chat_message(role):
            # Si es un mensaje del asistente y tiene información del modelo usado, mostrarla
            if role == "assistant" and "model_used" in msg:
                model_name = get_model_display_name(msg["model_used"])
                st.caption(f"Generado por: {model_name}")
                
                # Si el mensaje tiene herramientas ejecutadas, mostrar un indicador
                if "executed_tools" in msg and msg["executed_tools"]:
                    tool_count = len(msg["executed_tools"])
                    search_count = sum(1 for tool in msg["executed_tools"] if tool.get("type") == "search")
                    code_count = sum(1 for tool in msg["executed_tools"] if tool.get("type") == "code_execution")
                    
                    if search_count > 0 or code_count > 0:
                        tools_info = []
                        if search_count > 0:
                            tools_info.append(f"{search_count} búsquedas")
                        if code_count > 0:
                            tools_info.append(f"{code_count} ejecuciones de código")
                        
                        st.caption(f"Herramientas utilizadas: {', '.join(tools_info)}")
                        
                        # Mostrar las fuentes de las búsquedas en un expander
                        if search_count > 0:
                            with st.expander("Ver fuentes utilizadas", expanded=False):
                                for tool in msg["executed_tools"]:
                                    if tool.get("type") == "search":
                                        # Manejar input de forma segura (puede ser string o dict)
                                        tool_input = tool.get("input", {})
                                        if isinstance(tool_input, str):
                                            query = "Consulta desconocida"
                                        else:
                                            query = tool_input.get("query", "Consulta desconocida")
                                        
                                        st.markdown(f"**Búsqueda**: {query}")
                                        
                                        # Manejar output de forma segura (puede ser string o dict)
                                        tool_output = tool.get("output", {})
                                        if isinstance(tool_output, str):
                                            st.markdown("Formato de respuesta no compatible con visualización de fuentes")
                                            continue
                                        
                                        # Mostrar resultados y sus URLs
                                        results = tool_output.get("results", [])
                                        if results:
                                            for result in results:
                                                title = result.get("title", "Sin título")
                                                url = result.get("url", "#")
                                                st.markdown(f"- [{title}]({url})")
                                        else:
                                            st.markdown("No se encontraron resultados")
                                        
                                        st.markdown("---")
            
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
    
    # Añadir contexto de herramientas agénticas si está habilitado
    if session_state.context.get("enable_agentic", False):
        agentic_tools_manager = AgenticToolsManager(session_state)
        agentic_context = agentic_tools_manager.get_context_for_model()
        
        if agentic_context:
            api_messages.append({
                "role": "system",
                "content": f"Contexto adicional de búsquedas web y ejecuciones de código:\n\n{agentic_context}"
            })
            logger.info("Añadido contexto de herramientas agénticas a los mensajes")
    
    # Obtener el número máximo de mensajes a incluir según el modelo
    max_context_messages = get_context_limit(current_model)
    
    # Registrar el límite de contexto aplicado
    logger.info(f"Limitando contexto a {max_context_messages} mensajes para el modelo {current_model}")
    
    # Añadir mensajes del historial filtrando campos personalizados y limitando la cantidad
    # Tomamos solo los mensajes más recientes para no exceder los límites
    recent_messages = session_state.messages[-max_context_messages:] if len(session_state.messages) > max_context_messages else session_state.messages
    
    for msg in recent_messages:
        # Determinar el rol del mensaje (compatibilidad con formatos antiguos y nuevos)
        if "role" in msg and msg["role"] in ["user", "assistant"]:
            role = msg["role"]
        elif "is_user" in msg:
            role = "user" if msg["is_user"] else "assistant"
        else:
            # Si no se puede determinar el rol, omitir este mensaje
            continue
            
        # Solo incluir campos estándar (role y content)
        api_messages.append({"role": role, "content": msg["content"]})
    
    return api_messages

def display_agentic_context(session_state):
    """
    Muestra el contexto de herramientas agénticas en la interfaz.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
    """
    if not session_state.context.get("enable_agentic", False):
        return
    
    agentic_tools_manager = AgenticToolsManager(session_state)
    context = agentic_tools_manager.get_context_for_display()
    
    # Mostrar resultados de búsqueda
    if context["search_results"]:
        with st.expander("Resultados de búsqueda", expanded=False):
            for i, result in enumerate(context["search_results"]):
                st.markdown(f"### Búsqueda {i+1}: {result['query']}")
                for item in result['results']:
                    st.markdown(f"**{item.get('title', 'Sin título')}**")
                    st.markdown(f"{item.get('content', 'Sin contenido')}")
                    st.markdown(f"Fuente: [{item.get('url', 'Desconocida')}]({item.get('url', '#')})")
                    st.markdown("---")
    
    # Mostrar ejecuciones de código
    if context["code_executions"]:
        with st.expander("Ejecuciones de código", expanded=False):
            for i, execution in enumerate(context["code_executions"]):
                st.markdown(f"### Ejecución {i+1}")
                st.code(execution['code'], language="python")
                st.markdown("**Resultado:**")
                if execution['error']:
                    st.error(execution['error'])
                else:
                    st.code(execution['result'])
                st.markdown("---")

def handle_user_input(prompt, session_state, groq_client, logger):
    """
    Maneja la entrada del usuario y genera una respuesta.
    
    Args:
        prompt (str): Mensaje del usuario.
        session_state (SessionState): Estado de la sesión de Streamlit.
        groq_client (GroqClient): Cliente de la API de Groq.
        logger (logging.Logger): Logger para registrar información.
    """
    # Verificar si hay una transcripción de audio pendiente
    if hasattr(session_state, 'pending_audio_transcription') and session_state.pending_audio_transcription:
        audio_data = session_state.pending_audio_transcription
        session_state.pending_audio_transcription = None
        
        # Usar el texto transcrito como prompt
        prompt = f"[Transcripción de audio]: {audio_data['text']}"
        
        # Añadir el archivo temporal a la lista para limpieza posterior
        if 'temp_audio_files' not in session_state:
            session_state.temp_audio_files = []
        
        if 'path' in audio_data and audio_data['path']:
            session_state.temp_audio_files.append(audio_data['path'])
    
    # Verificar que tenemos una API key
    if not groq_client.is_configured():
        st.error("Por favor, ingresa tu API key de Groq en la barra lateral.")
        return
    
    # Obtener el modelo actual directamente del contexto
    current_model = session_state.context["model"]
    model_obj = get_model(current_model)
    is_agentic_model = hasattr(model_obj, "is_agentic") and model_obj.is_agentic
    supports_vision = hasattr(model_obj, "supports_vision") and model_obj.supports_vision
    
    # Verificación explícita del modelo actual
    logger.info(f"Verificando modelo seleccionado: {current_model} ({get_model_display_name(current_model)})")
    
    # Mostrar información del modelo que se está utilizando
    with st.chat_message("system"):
        st.info(f"Generando respuesta con {get_model_display_name(current_model)}...")
    
    # Agregar mensaje del usuario al historial
    session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar mensajes para la API
    api_messages = prepare_api_messages(session_state, current_model, logger)
    
    # Inicializar el gestor de herramientas agénticas si está habilitado
    agentic_tools_manager = None
    if session_state.context.get("enable_agentic", False):
        agentic_tools_manager = AgenticToolsManager(session_state)
    
    # Verificar si hay imágenes pendientes de procesar en el contexto
    has_pending_image = False
    pending_image = None
    if session_state.context.get("enable_vision", False) and supports_vision:
        if "image_context" in session_state and "recent_images" in session_state.image_context:
            for img in session_state.image_context["recent_images"]:
                if not img.get("processed", False):
                    has_pending_image = True
                    pending_image = img
                    break
    
    # Preparar instrucciones específicas para la imagen si es necesario
    image_instruction = ""
    if has_pending_image and pending_image:
        action = pending_image.get("action", "describe")
        if action == "describe":
            image_instruction = "Describe detalladamente la imagen que te muestro. Incluye todos los elementos visuales relevantes."
        elif action == "ocr":
            image_instruction = "Extrae todo el texto visible en la imagen. Organiza el texto de manera coherente, respetando la estructura original si es posible."
        
        # Marcar que estamos procesando esta imagen
        logger.info(f"Procesando imagen {pending_image['id']} con acción: {action}")
    
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
        
        # Generar respuesta (con o sin imagen)
        if has_pending_image and pending_image and session_state.context.get("enable_vision", False) and supports_vision:
            # Si hay una imagen pendiente, usar la API con soporte de visión
            logger.info(f"Generando respuesta con imagen usando modelo {current_model}")
            
            # Preparar datos de la imagen
            image_data = {
                "base64": pending_image["base64"]
            }
            
            # Si hay una instrucción específica para la imagen, reemplazar el último mensaje del usuario
            if image_instruction:
                # Reemplazar el último mensaje del usuario en los mensajes de la API
                for i in range(len(api_messages) - 1, -1, -1):
                    if api_messages[i]["role"] == "user":
                        api_messages[i]["content"] = image_instruction
                        break
            
            # Generar respuesta con imagen
            response = groq_client.generate_response_with_image(
                model=current_model,
                messages=api_messages,
                image_data=image_data,
                temperature=session_state.context["temperature"],
                max_tokens=session_state.context["max_tokens"],
                callback=update_response
            )
            
            # Marcar la imagen como procesada
            for img in session_state.image_context["recent_images"]:
                if img["id"] == pending_image["id"]:
                    img["processed"] = True
                    break
                    
        else:
            # Generar respuesta normal sin imagen
            response = groq_client.generate_streaming_response(
                model=current_model,
                messages=api_messages,
                temperature=session_state.context["temperature"],
                max_tokens=session_state.context["max_tokens"],
                callback=update_response
            )
        
        # Procesar la respuesta (ahora puede ser un diccionario con content y executed_tools)
        if isinstance(response, dict):
            content = response.get("content", "")
            executed_tools = response.get("executed_tools", [])
            
            # Procesar herramientas ejecutadas si hay un gestor de herramientas agénticas
            if agentic_tools_manager and executed_tools:
                logger.info(f"Procesando {len(executed_tools)} herramientas ejecutadas")
                agentic_tools_manager.process_executed_tools(executed_tools)
            
            # Mostrar la respuesta final
            model_info.empty()
            response_container.markdown(content)
            
            # Preparar el mensaje para el historial
            message_data = {
                "role": "assistant", 
                "content": content, 
                "model_used": current_model,
                "executed_tools": executed_tools
            }
            
            # Si se procesó una imagen, añadir información sobre ella
            if has_pending_image and pending_image:
                message_data["image_processed"] = True
                message_data["image_id"] = pending_image["id"]
                message_data["image_action"] = pending_image["action"]
                
                # Guardar la descripción de la imagen en el contexto
                if pending_image["action"] == "describe" and "image_descriptions" in session_state.image_context:
                    session_state.image_context["image_descriptions"].append({
                        "image_id": pending_image["id"],
                        "description": content
                    })
                    
                    # Limitar el número de descripciones almacenadas
                    if len(session_state.image_context["image_descriptions"]) > session_state.image_context["max_stored_images"]:
                        session_state.image_context["image_descriptions"].pop(0)
            
            # Agregar respuesta al historial
            session_state.messages.append(message_data)
        else:
            # Compatibilidad con versiones anteriores (si response es un string)
            model_info.empty()
            response_container.markdown(response)
            
            # Preparar el mensaje para el historial
            message_data = {
                "role": "assistant", 
                "content": response, 
                "model_used": current_model
            }
            
            # Si se procesó una imagen, añadir información sobre ella
            if has_pending_image and pending_image:
                message_data["image_processed"] = True
                message_data["image_id"] = pending_image["id"]
                message_data["image_action"] = pending_image["action"]
                
                # Guardar la descripción de la imagen en el contexto
                if pending_image["action"] == "describe" and "image_descriptions" in session_state.image_context:
                    session_state.image_context["image_descriptions"].append({
                        "image_id": pending_image["id"],
                        "description": response
                    })
                    
                    # Limitar el número de descripciones almacenadas
                    if len(session_state.image_context["image_descriptions"]) > session_state.image_context["max_stored_images"]:
                        session_state.image_context["image_descriptions"].pop(0)
            
            # Agregar respuesta al historial
            session_state.messages.append(message_data)
    
    # Ya no mostramos el contexto de herramientas agénticas en la interfaz
    # pero seguimos procesando la información para que el modelo pueda utilizarla
