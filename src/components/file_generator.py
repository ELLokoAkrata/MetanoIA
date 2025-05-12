"""
Componente para la generación y descarga de archivos.

Este módulo proporciona componentes de UI para solicitar la generación de archivos
en diferentes formatos (JSON, Python, Markdown y TXT) y descargarlos.
"""
import os
import streamlit as st
import base64
from typing import Dict, Any, List, Optional

def display_file_generator_info():
    """
    Muestra información sobre la funcionalidad de generación de archivos.
    """
    with st.expander("ℹ️ Sobre la generación de archivos"):
        st.markdown("""
        ### Generación de Archivos con MetanoIA
        
        Esta funcionalidad te permite generar archivos en diferentes formatos utilizando la API de Groq.
        
        **Formatos disponibles:**
        - **JSON**: Para datos estructurados (ej. configuraciones, datos)
        - **Python**: Para scripts y código ejecutable
        - **Markdown**: Para documentación y texto formateado
        - **TXT**: Para texto plano
        
        **¿Cómo funciona?**
        1. Solicita la generación de un archivo en el formato deseado
        2. El modelo de IA generará el contenido según tu solicitud
        3. Descarga el archivo generado con el botón correspondiente
        
        **Ejemplos de solicitudes:**
        - "Genera un archivo JSON con información de 3 libros de ciencia ficción"
        - "Crea un script Python que calcule números primos"
        - "Escribe un documento Markdown sobre inteligencia artificial"
        """)

def display_file_download(file_info: Dict[str, Any]):
    """
    Muestra un botón para descargar el archivo generado.
    
    Args:
        file_info (Dict[str, Any]): Información del archivo generado.
            Debe contener las claves: file_path, file_name, file_type, success.
    """
    if not file_info.get("success", False):
        st.error(f"Error al generar el archivo: {file_info.get('error', 'Error desconocido')}")
        return
    
    file_path = file_info.get("file_path")
    file_name = file_info.get("file_name")
    file_type = file_info.get("file_type")
    
    if not file_path or not os.path.exists(file_path):
        st.error(f"El archivo no existe en la ruta especificada: {file_path}")
        return
    
    # Leer el contenido del archivo
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    # Codificar el contenido en base64
    b64_content = base64.b64encode(file_content).decode()
    
    # Determinar el tipo MIME según el tipo de archivo
    mime_types = {
        "json": "application/json",
        "python": "text/x-python",
        "markdown": "text/markdown",
        "text": "text/plain"
    }
    mime_type = mime_types.get(file_type, "application/octet-stream")
    
    # Crear el botón de descarga
    download_button = f"""
    <a href="data:{mime_type};base64,{b64_content}" download="{file_name}" 
       style="display: inline-block; padding: 0.5em 1em; color: white; background-color: #4CAF50; 
              text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; 
              cursor: pointer; border-radius: 4px;">
        📥 Descargar {file_name}
    </a>
    """
    
    # Mostrar información del archivo y botón de descarga
    st.success(f"Archivo generado correctamente: {file_name}")
    
    # Mostrar una vista previa del contenido según el tipo de archivo
    with st.expander("👁️ Vista previa del contenido"):
        if file_type == "json":
            import json
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            st.json(content)
        elif file_type == "python":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language="python")
        elif file_type == "markdown":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)
        else:  # text
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.text(content)
    
    # Mostrar botón de descarga
    st.markdown(download_button, unsafe_allow_html=True)

def handle_file_generation_request(prompt: str, session_state, groq_client, file_generator, logger=None):
    """
    Maneja una solicitud de generación de archivo basada en el prompt del usuario.
    
    Args:
        prompt (str): Prompt del usuario solicitando la generación de un archivo.
        session_state: Estado de la sesión de Streamlit.
        groq_client: Cliente de Groq para realizar llamadas a la API.
        file_generator: Generador de archivos para crear los archivos solicitados.
        logger (optional): Logger para registrar información.
        
    Returns:
        bool: True si se detectó y procesó una solicitud de generación de archivo, False en caso contrario.
    """
    # Palabras clave que indican una solicitud de generación de archivo
    file_generation_keywords = [
        "genera", "generar", "crear", "crea", "hacer", "haz", "escribe", "escribir",
        "archivo", "fichero", "documento", "json", "python", "markdown", "txt", "texto",
        "código", "script", "programa", "documentación"
    ]
    
    # Verificar si el prompt contiene palabras clave de generación de archivo
    contains_keywords = any(keyword.lower() in prompt.lower() for keyword in file_generation_keywords)
    
    if not contains_keywords:
        return False
    
    # Obtener el modelo actual y parámetros de generación
    model = session_state.context.get("model", "llama-3.3-70b-versatile")
    temperature = session_state.context.get("temperature", 0.7)
    max_tokens = session_state.context.get("max_tokens", 4096)
    
    # Verificar si el modelo es compatible con herramientas
    compatible_models = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "meta-llama/llama-4-maverick-17b-128e-instruct",
        "qwen-qwq-32b",
        "deepseek-r1-distill-qwen-32b",
        "deepseek-r1-distill-llama-70b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it"
    ]
    
    if model not in compatible_models:
        st.warning(f"El modelo actual ({model}) no es compatible con la generación de archivos. Se utilizará llama-3.3-70b-versatile.")
        model = "llama-3.3-70b-versatile"
    
    # Preparar los mensajes para la API
    messages = [
        {
            "role": "system",
            "content": """Eres un asistente especializado en la generación de archivos. 
            Tu tarea es analizar la solicitud del usuario y generar el contenido adecuado 
            para el tipo de archivo solicitado. Utiliza las herramientas disponibles para 
            crear el archivo en el formato correcto. Asegúrate de que el contenido sea 
            relevante, bien estructurado y útil para el usuario."""
        }
    ]
    
    # Añadir mensajes del historial de chat si existen
    if "messages" in session_state and len(session_state.messages) > 0:
        # Añadir hasta 5 mensajes anteriores para dar contexto
        context_messages = session_state.messages[-5:] if len(session_state.messages) > 5 else session_state.messages
        for msg in context_messages:
            messages.append({
                "role": "user" if msg["is_user"] else "assistant",
                "content": msg["content"]
            })
    
    # Añadir el prompt actual
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Obtener las definiciones de herramientas
    tools = file_generator.get_tools_definitions()
    
    # Mostrar mensaje de procesamiento
    with st.spinner("Analizando solicitud y generando archivo..."):
        # Realizar la llamada a la API con herramientas
        response = groq_client.generate_response_with_tools(
            model=model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Verificar si se realizaron llamadas a herramientas
        tool_calls = response.get("tool_calls", [])
        
        if not tool_calls:
            # No se detectó una solicitud de generación de archivo válida
            if logger:
                logger.info("No se detectó una solicitud de generación de archivo válida")
            return False
        
        # Procesar las llamadas a herramientas
        available_functions = file_generator.get_available_functions()
        
        final_response = groq_client.process_tool_calls(
            model=model,
            messages=messages,
            tool_calls=tool_calls,
            available_functions=available_functions,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Mostrar los resultados de las herramientas
        tool_results = final_response.get("tool_results", [])
        
        for result in tool_results:
            if result.get("success", False):
                # Mostrar botón de descarga para el archivo generado
                display_file_download(result)
                
                # Añadir el archivo a la lista de archivos temporales para limpieza posterior
                if "temp_files" not in session_state:
                    session_state.temp_files = []
                session_state.temp_files.append(result.get("file_path"))
        
        # Añadir mensaje al historial de chat
        if "messages" not in session_state:
            session_state.messages = []
        
        # Añadir el prompt del usuario
        session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Añadir la respuesta del asistente
        session_state.messages.append({
            "role": "assistant",
            "content": final_response.get("content", "Se ha generado el archivo solicitado."),
            "model_used": model  # Añadir información del modelo utilizado
        })
        
        return True
