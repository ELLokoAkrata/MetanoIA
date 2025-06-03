"""
Módulo para la barra lateral de la aplicación.
"""
import streamlit as st
import os
import uuid
from src.models.config import AVAILABLE_MODELS, get_model
from src.utils.agentic_tools_manager import AgenticToolsManager
from src.utils.image_processor import resize_image, encode_image_to_base64, save_uploaded_image
from src.components.file_processor import display_file_uploader

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
    # Inicializar el gestor de herramientas agénticas
    agentic_tools_manager = AgenticToolsManager(session_state)
    
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
        
        # Usar key dinámica para forzar la recreación del widget cuando cambia el modelo
        selected_model = st.selectbox(
            "Selecciona un modelo",
            options=list(AVAILABLE_MODELS.keys()),
            format_func=lambda x: AVAILABLE_MODELS[x],
            index=list(AVAILABLE_MODELS.keys()).index(session_state.context["model"]) 
                if session_state.context["model"] in AVAILABLE_MODELS else 0,
            key=f"model_select_{session_state.context['model']}"
        )
        
        # Mostrar información sobre el modelo actual
        if selected_model == session_state.context["model"]:
            st.success(f"Usando modelo: {AVAILABLE_MODELS[selected_model]}")
        else:
            st.warning(f"Cambiando de {AVAILABLE_MODELS[session_state.context['model']]} a {AVAILABLE_MODELS[selected_model]}...")
        
        # Verificar si el modelo seleccionado es agéntico o soporta visión
        model_obj = get_model(selected_model)
        is_agentic_model = hasattr(model_obj, "is_agentic") and model_obj.is_agentic
        supports_vision = hasattr(model_obj, "supports_vision") and model_obj.supports_vision
        
        # Configuración de herramientas agénticas
        if is_agentic_model:
            st.info("Has seleccionado un modelo con capacidades agénticas que puede buscar en internet y ejecutar código.")
        
        # Activar/desactivar herramientas agénticas
        enable_agentic = st.checkbox(
            "Activar herramientas agénticas",
            value=session_state.context.get("enable_agentic", False),
            help="Permite que el modelo busque información en internet y ejecute código Python."
        )
        
        # Configuración de procesamiento de imágenes
        if supports_vision:
            st.info("Has seleccionado un modelo con capacidades de visión que puede analizar imágenes.")
            
            # Activar/desactivar visión
            enable_vision = st.checkbox(
                "Activar procesamiento de imágenes",
                value=session_state.context.get("enable_vision", False),
                help="Permite que el modelo analice imágenes y extraiga información de ellas."
            )
            
            # Opciones de procesamiento de imágenes
            if enable_vision:
                st.subheader("Procesamiento de Imágenes")
                
                # Cargar imagen
                uploaded_file = st.file_uploader(
                    "Cargar imagen", 
                    type=["jpg", "jpeg", "png"],
                    help="Sube una imagen para que el modelo la analice."
                )
                
                if uploaded_file is not None:
                    # Mostrar la imagen
                    st.image(uploaded_file, caption="Imagen cargada", width=300)
                    
                    # Guardar la imagen en el sistema de archivos
                    image_id = str(uuid.uuid4())
                    image_path = save_uploaded_image(uploaded_file, image_id)
                    
                    # Procesar la imagen
                    col1, col2 = st.columns(2)
                    
                    if col1.button("Describir imagen"):
                        try:
                            # Redimensionar y codificar la imagen
                            resized_image_path = resize_image(image_path)
                            base64_image = encode_image_to_base64(resized_image_path)
                            
                            # Guardar en el contexto de sesión
                            if "recent_images" not in session_state.image_context:
                                session_state.image_context["recent_images"] = []
                            
                            # Añadir la imagen al contexto
                            session_state.image_context["recent_images"].append({
                                "id": image_id,
                                "path": image_path,
                                "base64": base64_image,
                                "action": "describe",
                                "processed": False
                            })
                            
                            # Limitar el número de imágenes almacenadas
                            if len(session_state.image_context["recent_images"]) > session_state.image_context["max_stored_images"]:
                                # Eliminar la imagen más antigua y su archivo
                                oldest_image = session_state.image_context["recent_images"].pop(0)
                                if os.path.exists(oldest_image["path"]):
                                    os.remove(oldest_image["path"])
                            
                            st.success("Imagen lista para ser analizada. Escribe un mensaje en el chat para obtener una descripción.")
                            
                        except Exception as e:
                            st.error(f"Error al procesar la imagen: {str(e)}")
                            logger.error(f"Error al procesar imagen: {str(e)}")
                    
                    if col2.button("Extraer texto (OCR)"):
                        try:
                            # Redimensionar y codificar la imagen
                            resized_image_path = resize_image(image_path)
                            base64_image = encode_image_to_base64(resized_image_path)
                            
                            # Guardar en el contexto de sesión
                            if "recent_images" not in session_state.image_context:
                                session_state.image_context["recent_images"] = []
                            
                            # Añadir la imagen al contexto
                            session_state.image_context["recent_images"].append({
                                "id": image_id,
                                "path": image_path,
                                "base64": base64_image,
                                "action": "ocr",
                                "processed": False
                            })
                            
                            # Limitar el número de imágenes almacenadas
                            if len(session_state.image_context["recent_images"]) > session_state.image_context["max_stored_images"]:
                                # Eliminar la imagen más antigua y su archivo
                                oldest_image = session_state.image_context["recent_images"].pop(0)
                                if os.path.exists(oldest_image["path"]):
                                    os.remove(oldest_image["path"])
                            
                            st.success("Imagen lista para extraer texto. Escribe un mensaje en el chat para obtener el texto extraído.")
                            
                        except Exception as e:
                            st.error(f"Error al procesar la imagen: {str(e)}")
                            logger.error(f"Error al procesar imagen: {str(e)}")
        else:
            # Si el modelo no soporta visión, desactivar la opción
            enable_vision = False
        
        # Configuración de búsqueda web
        if enable_agentic:
            st.subheader("Configuración de Búsqueda Web")
            
            search_depth = st.selectbox(
                "Profundidad de búsqueda",
                options=["basic", "advanced"],
                index=0 if session_state.agentic_context["search_settings"]["search_depth"] == "basic" else 1,
                format_func=lambda x: "Básica" if x == "basic" else "Avanzada",
                help="Básica: búsqueda rápida. Avanzada: búsqueda más profunda pero más lenta."
            )
            
            max_results = st.slider(
                "Máximo de resultados",
                min_value=1,
                max_value=10,
                value=session_state.agentic_context["search_settings"]["max_results"],
                help="Número máximo de resultados de búsqueda a mostrar."
            )
            
            include_domains = st.text_input(
                "Dominios a incluir (separados por comas)",
                value=",".join(session_state.agentic_context["search_settings"]["include_domains"]),
                help="Dominios específicos en los que buscar, ej: wikipedia.org,gov.org"
            )
            
            exclude_domains = st.text_input(
                "Dominios a excluir (separados por comas)",
                value=",".join(session_state.agentic_context["search_settings"]["exclude_domains"]),
                help="Dominios a excluir de la búsqueda, ej: pinterest.com,instagram.com"
            )
            
            # Actualizar configuración de búsqueda
            agentic_tools_manager.update_search_settings({
                "search_depth": search_depth,
                "max_results": max_results,
                "include_domains": [domain.strip() for domain in include_domains.split(",") if domain.strip()],
                "exclude_domains": [domain.strip() for domain in exclude_domains.split(",") if domain.strip()]
            })
        
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

        display_file_uploader(session_state, logger)
        
        # Detectar cambios en la configuración
        config_changed = False
        
        # Actualizar contexto cuando cambian los valores
        if (selected_model != session_state.context["model"]):
            logger.info(f"Cambio de modelo: {session_state.context['model']} -> {selected_model}")
            session_state.context["model"] = selected_model
            config_changed = True
            
            # Forzar reinicio inmediato cuando cambia el modelo
            # Esto garantiza que el cambio se aplique correctamente
            logger.info("Forzando reinicio de la aplicación para aplicar el cambio de modelo")
            st.rerun()
        
        if (temperature != session_state.context["temperature"] or
            max_tokens != session_state.context["max_tokens"] or
            system_prompt != session_state.context["system_prompt"] or
            enable_agentic != session_state.context.get("enable_agentic", False) or
            (supports_vision and enable_vision != session_state.context.get("enable_vision", False))):
            
            logger.info(f"Cambio de parámetros: temperatura={temperature}, max_tokens={max_tokens}, enable_agentic={enable_agentic}, enable_vision={enable_vision if supports_vision else False}")
            session_state.context["temperature"] = temperature
            session_state.context["max_tokens"] = max_tokens
            session_state.context["system_prompt"] = system_prompt
            session_state.context["enable_agentic"] = enable_agentic
            if supports_vision:
                session_state.context["enable_vision"] = enable_vision
            config_changed = True
        
        # Botones de acción
        st.subheader("Acciones")
        col1, col2 = st.columns(2)
        
        # Botón para limpiar la conversación
        if col1.button("Limpiar conversación"):
            logger.info("Conversación limpiada")
            session_state.messages = []
            return True
        
        # Botón para limpiar el contexto agéntico
        if col2.button("Limpiar contexto agéntico"):
            logger.info("Contexto agéntico limpiado")
            agentic_tools_manager.clear_context()
            return True
        
        return config_changed
