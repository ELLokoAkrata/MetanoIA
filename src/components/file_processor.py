"""Componente para la subida y procesamiento de archivos."""

import streamlit as st
from typing import Any, Dict

from src.api.file_processor import FileProcessor


def display_file_uploader(session_state, logger=None) -> None:
    """Muestra un cargador de archivos y procesa su contenido.

    Este componente permite subir archivos en formato PDF, TXT o JSON,
    procesarlos con :class:`FileProcessor` y añadir la información
    obtenida al contexto general de la conversación. Tras procesar un
    archivo, el usuario puede reiniciar el cargador para subir otro sin
    modificar directamente ``st.session_state``.

    Args:
        session_state: Estado de la sesión de Streamlit.
        logger (logging.Logger, optional): Logger para registrar eventos.
    """
    st.subheader("Procesamiento de Archivos")
    uploader_key = f"file_processor_uploader_{session_state.get('file_uploader_counter', 0)}"

    uploaded_file = st.file_uploader(
        "Selecciona un archivo", type=["pdf", "txt", "json"], key=uploader_key
    )

    if uploaded_file is None:
        return

    file_bytes = uploaded_file.getvalue()
    extension = uploaded_file.name.split(".")[-1].lower()
    processor = FileProcessor(logger=logger)
    result = processor.process_file(file_bytes, extension)

    if result.get("success"):
        st.success(f"Archivo '{uploaded_file.name}' procesado correctamente.")
        file_info: Dict[str, Any] = {
            "file_name": uploaded_file.name,
            "file_type": extension,
            "content": result["content"],
        }
        session_state.processed_files = session_state.get("processed_files", [])
        session_state.processed_files.append(file_info)

        if "messages" not in session_state:
            session_state.messages = []
            
        # Crear un identificador único para este archivo
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

        if st.button("Procesar otro archivo"):
            session_state.file_uploader_counter = session_state.get("file_uploader_counter", 0) + 1
            if logger:
                logger.info("Reiniciando cargador de archivos")
            st.rerun()
    else:
        st.error(f"Error al procesar el archivo: {result.get('error', 'desconocido')}")
