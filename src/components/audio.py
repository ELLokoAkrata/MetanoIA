"""
Módulo para el componente de audio de la aplicación.
"""
import streamlit as st
import tempfile
import os

def display_audio_input(session_state):
    """
    Muestra los controles para subir o grabar audio y transcribirlo.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
    
    Returns:
        dict or None: Información del audio si se ha subido/grabado, None en caso contrario.
    """
    audio_data = None
    
    # Crear un expander para los controles de audio
    with st.expander("🎤 Entrada de voz", expanded=False):
        st.markdown("### Transcripción de voz a texto")
        
        # Pestañas para elegir entre subir archivo o grabar
        tab1, tab2 = st.tabs(["Subir archivo de audio", "Grabar audio"])
        
        with tab1:
            uploaded_file = st.file_uploader(
                "Sube un archivo de audio (mp3, wav, etc.)", 
                type=["mp3", "wav", "m4a", "flac", "ogg"],
                key="audio_uploader"
            )
            
            if uploaded_file is not None:
                # Mostrar reproductor de audio
                st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[1]}")
                
                # Guardar el archivo temporalmente
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_path = tmp_file.name
                
                # Opciones de transcripción
                col1, col2 = st.columns(2)
                with col1:
                    model = st.selectbox(
                        "Modelo de transcripción",
                        ["whisper-large-v3-turbo", "whisper-large-v3", "distil-whisper-large-v3-en"],
                        index=0,
                        key="transcription_model"
                    )
                with col2:
                    language = st.selectbox(
                        "Idioma (opcional)",
                        ["", "es", "en", "fr", "de", "it", "pt", "ru", "zh", "ja"],
                        index=1,  # Español por defecto
                        key="transcription_language"
                    )
                
                # Botón para transcribir
                if st.button("Transcribir audio", key="transcribe_button"):
                    audio_data = {
                        "type": "file",
                        "path": temp_path,
                        "model": model,
                        "language": language if language else None,
                        "action": "transcribe"
                    }
        
        with tab2:
            st.info("La grabación de audio directa no está disponible en esta versión de Streamlit. Por favor, utiliza la opción de subir un archivo de audio.")
            
            # Mostrar instrucciones alternativas
            st.markdown("""
            ### Alternativas para grabar audio:
            1. Usa una aplicación de grabación en tu dispositivo (como la Grabadora de Voz de Windows)
            2. Guarda el archivo de audio
            3. Súbelo usando la pestaña 'Subir archivo de audio'
            """)
    
    return audio_data

def cleanup_temp_files(session_state):
    """
    Limpia los archivos temporales de audio.
    
    Args:
        session_state (SessionState): Estado de la sesión de Streamlit.
    """
    if "temp_audio_files" in session_state and session_state.temp_audio_files:
        for file_path in session_state.temp_audio_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                st.error(f"Error al eliminar archivo temporal: {str(e)}")
        
        # Limpiar la lista después de eliminar
        session_state.temp_audio_files = []
