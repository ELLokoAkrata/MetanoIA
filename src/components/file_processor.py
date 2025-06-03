"""Componente para la subida y procesamiento de archivos."""

import streamlit as st
from typing import Any, Dict

from src.api.file_processor import FileProcessor


def display_file_uploader(session_state, logger=None) -> None:
    """Muestra un cargador de archivos y procesa su contenido.

    Este componente permite subir archivos en formato PDF, TXT o JSON,
    procesarlos con :class:`FileProcessor` y añadir la información
    obtenida al contexto general de la conversación.

    Args:
        session_state: Estado de la sesión de Streamlit.
        logger (logging.Logger, optional): Logger para registrar eventos.
    """
    st.subheader("Procesamiento de Archivos")
    uploaded_file = st.file_uploader(
        "Selecciona un archivo", type=["pdf", "txt", "json"]
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
        session_state.messages.append(
            {
                "role": "system",
                "content": (
                    f"El usuario ha subido el archivo {uploaded_file.name} "
                    f"de tipo {extension}.\nContenido procesado:\n{result['content']}"
                ),
            }
        )
    else:
        st.error(f"Error al procesar el archivo: {result.get('error', 'desconocido')}")
