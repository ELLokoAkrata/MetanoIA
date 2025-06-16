"""Componente para la subida y procesamiento de archivos.

Este módulo proporciona las funciones necesarias para que el usuario
suba archivos y se integren en el contexto de conversación. Se
almacenan los archivos procesados en ``st.session_state`` y se evita el
procesamiento duplicado mediante un identificador único por archivo.
"""

import hashlib
import streamlit as st
from typing import Any, Dict

from src.api.file_processor import FileProcessor


def _generate_file_hash(data: bytes) -> str:
    """Genera un hash SHA256 a partir de los bytes del archivo.

    Args:
        data: Datos binarios del archivo.

    Returns:
        str: Representación hexadecimal del hash.
    """

    return hashlib.sha256(data).hexdigest()


def display_file_uploader(session_state, logger=None) -> None:
    """Muestra un cargador de archivos y procesa su contenido.

    Este componente permite subir archivos en formato PDF, TXT o JSON y
    utiliza :class:`FileProcessor` para extraer su información. Para cada
    archivo se calcula un hash que se almacena en
    ``session_state.processed_files`` con el fin de detectar duplicados en
    recargas posteriores. Si se intenta procesar un archivo ya
    registrado, se omite el procesamiento y se notifica al usuario.

    Args:
        session_state: Estado de la sesión de Streamlit.
        logger (logging.Logger, optional): Logger para registrar eventos.
    """
    st.subheader("Procesamiento de Archivos")
    uploaded_file = st.file_uploader(
        "Selecciona un archivo", type=["pdf", "txt", "json"], key="file_processor_uploader"
    )

    if uploaded_file is None:
        return

    file_bytes = uploaded_file.getvalue()
    file_hash = _generate_file_hash(file_bytes)
    extension = uploaded_file.name.split(".")[-1].lower()

    # Verificar si el archivo ya fue procesado
    processed_files = session_state.get("processed_files", [])
    if any(info.get("file_hash") == file_hash for info in processed_files):
        st.info(f"El archivo '{uploaded_file.name}' ya fue procesado. Se omite.")
        if logger:
            logger.info(f"Procesamiento omitido para archivo duplicado: {uploaded_file.name} ({file_hash})")
        st.session_state["file_processor_uploader"] = None
        return

    processor = FileProcessor(logger=logger)
    result = processor.process_file(file_bytes, extension)

    if result.get("success"):
        st.success(f"Archivo '{uploaded_file.name}' procesado correctamente.")
        file_info: Dict[str, Any] = {
            "file_name": uploaded_file.name,
            "file_type": extension,
            "file_size": len(file_bytes),
            "file_hash": file_hash,
            "content": result["content"],
        }
        session_state.processed_files = session_state.get("processed_files", [])
        session_state.processed_files.append(file_info)

        if "messages" not in session_state:
            session_state.messages = []
            
        # Crear un identificador secuencial para este archivo
        file_id = f"file_{len(session_state.processed_files)}"
        file_info["file_id"] = file_id
        
        # Añadir mensaje del sistema con formato mejorado para que el modelo lo reconozca
        session_state.messages.append(
            {
                "role": "system",
                "content": (
                    f"### ARCHIVO PROCESADO (ID: {file_id}) ###\n\n"
                    f"Nombre: {uploaded_file.name}\n"
                    f"Tipo: {extension}\n"
                    f"Contenido:\n\n```{extension}\n{result['content']}\n```\n\n"
                    f"El usuario puede referirse a este archivo en la conversación. "
                    f"Debes utilizar la información de este archivo para responder a sus preguntas."
                ),
            }
        )

        # Mostrar una vista previa del contenido procesado
        with st.expander(f"Vista previa del contenido procesado de {uploaded_file.name}"):
            if extension == "json":
                st.json(result["content"])
            else:
                st.text_area("Contenido:", value=result["content"], height=200, disabled=True)

        # Limpiar el valor del uploader para evitar reprocesar en recargas
        st.session_state["file_processor_uploader"] = None
    else:
        st.error(f"Error al procesar el archivo: {result.get('error', 'desconocido')}")
