"""
Módulo para la transcripción de audio utilizando la API de Groq.
"""
import os
import time
import requests
import json

class AudioTranscriber:
    """
    Clase para manejar la transcripción de audio utilizando la API de Groq.
    """
    def __init__(self, groq_client, logger=None):
        """
        Inicializa el transcriptor de audio.
        
        Args:
            groq_client (GroqClient): Cliente de Groq ya configurado.
            logger (logging.Logger, optional): Logger para registrar información.
        """
        self.groq_client = groq_client
        self.logger = logger
        self.transcription_endpoint = "https://api.groq.com/openai/v1/audio/transcriptions"
        self.translation_endpoint = "https://api.groq.com/openai/v1/audio/translations"
        
    def transcribe_audio(self, audio_path, model="whisper-large-v3-turbo", language=None, response_format="json"):
        """
        Transcribe un archivo de audio utilizando la API de Groq.
        
        Args:
            audio_path (str): Ruta al archivo de audio a transcribir.
            model (str): Modelo de Whisper a utilizar.
            language (str, optional): Código de idioma (ej. "es", "en").
            response_format (str): Formato de respuesta ("text", "json", "verbose_json").
            
        Returns:
            dict: Resultado de la transcripción con el texto y metadatos.
        """
        if not self.groq_client.is_configured():
            error_msg = "Error: API no configurada. Por favor, proporciona una clave API."
            if self.logger:
                self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        try:
            if self.logger:
                self.logger.info(f"Iniciando transcripción de audio: {os.path.basename(audio_path)}")
                self.logger.info(f"Modelo: {model}, Idioma: {language or 'auto'}")
            
            start_time = time.time()
            
            # Obtener la clave API del cliente de Groq
            api_key = self.groq_client.api_key
            
            # Preparar los headers para la solicitud
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            # Preparar los datos para la solicitud
            files = {
                "file": (os.path.basename(audio_path), open(audio_path, "rb"))
            }
            
            # Importante: Siempre usar formato JSON para la respuesta para facilitar el procesamiento
            data = {
                "model": model,
                "response_format": "json"  # Forzar formato JSON para mejor manejo
            }
            
            # Añadir parámetros opcionales si están presentes
            if language:
                data["language"] = language
            
            # Realizar la solicitud HTTP directamente al endpoint de transcripción
            response = requests.post(
                self.transcription_endpoint,
                headers=headers,
                files=files,
                data=data
            )
            
            elapsed_time = time.time() - start_time
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                try:
                    # Procesar la respuesta JSON
                    response_data = response.json()
                    
                    # Extraer el texto transcrito
                    transcribed_text = response_data.get("text", "")
                    
                    if self.logger:
                        self.logger.info(f"Transcripción completada en {elapsed_time:.2f} segundos")
                        self.logger.info(f"Longitud del texto transcrito: {len(transcribed_text)} caracteres")
                        self.logger.info(f"Primeros 100 caracteres: {transcribed_text[:100]}...")
                    
                    result = {
                        "success": True,
                        "text": transcribed_text,
                        "model_used": model,
                        "duration_seconds": elapsed_time,
                        "data": response_data
                    }
                except Exception as e:
                    # Si hay un error al procesar el JSON, intentar usar la respuesta como texto
                    error_msg = f"Error al procesar la respuesta JSON: {str(e)}"
                    if self.logger:
                        self.logger.error(error_msg)
                        self.logger.info(f"Intentando usar la respuesta como texto plano")
                    
                    result = {
                        "success": True,
                        "text": response.text.strip(),
                        "model_used": model,
                        "duration_seconds": elapsed_time
                    }
            else:
                # Si hubo un error, devolver la información del error
                error_msg = f"Error en la API de Groq: {response.status_code} - {response.text}"
                if self.logger:
                    self.logger.error(error_msg)
                
                result = {
                    "success": False,
                    "error": error_msg,
                    "status_code": response.status_code
                }
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la transcripción: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
                self.logger.exception("Detalles del error:")
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def translate_audio(self, audio_path, model="whisper-large-v3", response_format="json"):
        """
        Traduce un archivo de audio a inglés utilizando la API de Groq.
        
        Args:
            audio_path (str): Ruta al archivo de audio a traducir.
            model (str): Modelo de Whisper a utilizar.
            response_format (str): Formato de respuesta ("text", "json", "verbose_json").
            
        Returns:
            dict: Resultado de la traducción con el texto y metadatos.
        """
        if not self.groq_client.is_configured():
            error_msg = "Error: API no configurada. Por favor, proporciona una clave API."
            if self.logger:
                self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
        
        try:
            if self.logger:
                self.logger.info(f"Iniciando traducción de audio: {os.path.basename(audio_path)}")
                self.logger.info(f"Modelo: {model}")
            
            start_time = time.time()
            
            # Obtener la clave API del cliente de Groq
            api_key = self.groq_client.api_key
            
            # Preparar los headers para la solicitud
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            # Preparar los datos para la solicitud
            files = {
                "file": (os.path.basename(audio_path), open(audio_path, "rb"))
            }
            
            # Importante: Siempre usar formato JSON para la respuesta para facilitar el procesamiento
            data = {
                "model": model,
                "response_format": "json"  # Forzar formato JSON para mejor manejo
            }
            
            # Realizar la solicitud HTTP directamente al endpoint de traducción
            response = requests.post(
                self.translation_endpoint,
                headers=headers,
                files=files,
                data=data
            )
            
            elapsed_time = time.time() - start_time
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                try:
                    # Procesar la respuesta JSON
                    response_data = response.json()
                    
                    # Extraer el texto traducido
                    translated_text = response_data.get("text", "")
                    
                    if self.logger:
                        self.logger.info(f"Traducción completada en {elapsed_time:.2f} segundos")
                        self.logger.info(f"Longitud del texto traducido: {len(translated_text)} caracteres")
                        self.logger.info(f"Primeros 100 caracteres: {translated_text[:100]}...")
                    
                    result = {
                        "success": True,
                        "text": translated_text,
                        "model_used": model,
                        "duration_seconds": elapsed_time,
                        "data": response_data
                    }
                except Exception as e:
                    # Si hay un error al procesar el JSON, intentar usar la respuesta como texto
                    error_msg = f"Error al procesar la respuesta JSON: {str(e)}"
                    if self.logger:
                        self.logger.error(error_msg)
                        self.logger.info(f"Intentando usar la respuesta como texto plano")
                    
                    result = {
                        "success": True,
                        "text": response.text.strip(),
                        "model_used": model,
                        "duration_seconds": elapsed_time
                    }
            else:
                # Si hubo un error, devolver la información del error
                error_msg = f"Error en la API de Groq: {response.status_code} - {response.text}"
                if self.logger:
                    self.logger.error(error_msg)
                
                result = {
                    "success": False,
                    "error": error_msg,
                    "status_code": response.status_code
                }
            
            return result
            
        except Exception as e:
            error_msg = f"Error en la traducción: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
                self.logger.exception("Detalles del error:")
            
            return {
                "success": False,
                "error": error_msg
            }
