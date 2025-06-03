"""
MetanoIA: Un chatbot modular con múltiples modelos de lenguaje.

Esta aplicación permite interactuar con diferentes modelos de lenguaje a través 
de una interfaz de chat moderna y configurable, manteniendo el contexto de la 
conversación al cambiar entre modelos.
"""
import streamlit as st
import os
import tempfile

# Importar módulos propios
from src.utils.logger import setup_logger
from src.utils.styles import apply_fresh_tech_theme
from src.utils.session_state import initialize_session_state, cleanup_temp_files
from src.models.config import AVAILABLE_MODELS
from src.api.groq_client import GroqClient
from src.components.sidebar import render_sidebar
from src.components.chat import display_chat_history, handle_user_input, display_agentic_context
from src.components.audio import display_audio_input
from src.components.file_generator import display_file_generator_info, handle_file_generation_request
from src.api.audio_transcription import AudioTranscriber
from src.api.file_generator import FileGenerator

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
    
    # Inicializar el generador de archivos
    temp_dir = os.path.join(tempfile.gettempdir(), "metanoia_files")
    os.makedirs(temp_dir, exist_ok=True)
    file_generator = FileGenerator(temp_dir=temp_dir, logger=logger)
    
    # Título principal
    st.title("🤖 MetanoIA")
    st.markdown("Chat bot modular usando Streamlit y la API de Groq")
    
    # Mostrar indicador del modelo actual
    from src.models.config import get_model_display_name
    st.markdown(f"**Modelo actual:** {get_model_display_name(session_state.context['model'])}")
    
    # Renderizar la barra lateral
    config_changed = render_sidebar(session_state, groq_client, logger)
    
    # Si la configuración cambió, recargar la página
    if config_changed:
        st.rerun()
    
    # Mostrar información sobre la generación de archivos
    display_file_generator_info()

    # Mostrar archivos procesados si existen
    if session_state.processed_files:
        st.subheader("📄 Archivos procesados")
        for file in session_state.processed_files:
            label = f"{file['file_name']} ({file['file_type']})"
            with st.expander(label, expanded=False):
                if file["file_type"] == "json":
                    st.json(file["content"])
                else:
                    st.text(file["content"])
    
    # Procesar entrada de audio si está habilitada
    audio_data = display_audio_input(session_state)
    if audio_data:
        # Mostrar mensaje de procesamiento
        with st.spinner(f"Transcribiendo audio con {audio_data['model']}..."):
            # Inicializar el transcriptor de audio
            transcriber = AudioTranscriber(groq_client, logger)
            
            # Transcribir el audio
            result = transcriber.transcribe_audio(
                audio_path=audio_data['path'],
                model=audio_data['model'],
                language=audio_data['language']
            )
            
            if result['success']:
                # Mostrar el texto transcrito directamente en la interfaz
                st.success("Audio transcrito correctamente")
                
                # Mostrar el texto transcrito con un botón de copia fácil
                transcribed_text = result['text']
                
                # Mostrar el texto en un bloque de código con botón de copia
                st.code(transcribed_text, language=None)
                
                # Guardar el archivo temporal para limpieza posterior
                if 'temp_audio_files' not in session_state:
                    session_state.temp_audio_files = []
                session_state.temp_audio_files.append(audio_data['path'])
            else:
                st.error(f"Error al transcribir el audio: {result.get('error', 'Error desconocido')}")
    
    # Limpiar archivos temporales al final de la sesión
    cleanup_temp_files(session_state)
    
    # Contenedor principal del chat
    chat_container = st.container()
    
    # Mostrar mensajes anteriores
    with chat_container:
        display_chat_history(session_state, AVAILABLE_MODELS)
    
    # Entrada de usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        # Verificar si es una solicitud de generación de archivo
        is_file_request = handle_file_generation_request(prompt, session_state, groq_client, file_generator, logger)
        
        # Si no es una solicitud de generación de archivo, manejar como un mensaje normal
        if not is_file_request:
            handle_user_input(prompt, session_state, groq_client, logger)

if __name__ == "__main__":
    main()
