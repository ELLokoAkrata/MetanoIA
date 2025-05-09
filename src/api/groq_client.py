"""
Módulo para interactuar con la API de Groq.
"""
import os
import time
import streamlit as st
from groq import Groq
from src.api.base_client import BaseAPIClient

class GroqClient(BaseAPIClient):
    """
    Cliente para interactuar con la API de Groq.
    Implementa la interfaz definida en BaseAPIClient.
    """
    def __init__(self, api_key=None, logger=None):
        """
        Inicializa el cliente de Groq.
        
        Args:
            api_key (str, optional): Clave API de Groq. Si no se proporciona, 
                                     se intenta obtener de las variables de entorno.
            logger (logging.Logger, optional): Logger para registrar información.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.logger = logger
        self.client = None
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        
    def is_configured(self):
        """
        Verifica si el cliente está configurado correctamente.
        
        Returns:
            bool: True si el cliente está configurado, False en caso contrario.
        """
        return self.client is not None and self.api_key is not None
    
    def set_api_key(self, api_key):
        """
        Establece la clave API y reconfigura el cliente.
        
        Args:
            api_key (str): Clave API de Groq.
        """
        self.api_key = api_key
        os.environ["GROQ_API_KEY"] = api_key
        self.client = Groq(api_key=self.api_key)
        
        if self.logger:
            self.logger.info("API key configurada")
    
    # Función cacheada para obtener respuestas que no cambiarán con los mismos parámetros
    @st.cache_data(ttl=3600, show_spinner=False)
    def _cached_api_call(self, model, messages_str, temperature, max_tokens):
        """
        Realiza una llamada a la API con caché.
        
        Args:
            model (str): ID del modelo a utilizar.
            messages_str (str): Representación en string de los mensajes (para caché).
            temperature (float): Temperatura para la generación.
            max_tokens (int): Número máximo de tokens en la respuesta.
            
        Returns:
            str: Contenido de la respuesta o mensaje de error.
        """
        try:
            # Convertir la representación de string a lista de mensajes
            import json
            messages = json.loads(messages_str)
            
            if self.logger:
                self.logger.info(f"Llamada a API CACHEADA con modelo: {model}")
            
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            elapsed_time = time.time() - start_time
            
            if self.logger:
                self.logger.info(f"Respuesta cacheada recibida en {elapsed_time:.2f} segundos")
            
            return response.choices[0].message.content
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en llamada API cacheada: {str(e)}")
            return f"Error al llamar a la API: {str(e)}"
    
    def get_cached_response(self, model, messages, temperature, max_tokens):
        """
        Obtiene una respuesta cacheada para parámetros específicos.
        
        Args:
            model (str): ID del modelo a utilizar.
            messages (list): Lista de mensajes para la conversación.
            temperature (float): Temperatura para la generación.
            max_tokens (int): Número máximo de tokens en la respuesta.
            
        Returns:
            str: Contenido de la respuesta o mensaje de error.
        """
        if not self.is_configured():
            return "Error: API no configurada. Por favor, proporciona una clave API."
        
        try:
            # Convertir mensajes a string para la caché
            import json
            messages_str = json.dumps(messages)
            
            if self.logger:
                self.logger.info(f"Preparando llamada cacheada: {model}, temperatura: {temperature}, max_tokens: {max_tokens}")
            
            # Usar la función cacheada
            return self._cached_api_call(model, messages_str, temperature, max_tokens)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error al preparar llamada cacheada: {str(e)}")
            return f"Error al llamar a la API: {str(e)}"
    
    def generate_streaming_response(self, model, messages, temperature, max_tokens, callback=None):
        """
        Genera una respuesta en streaming para una experiencia más interactiva.
        
        Args:
            model (str): ID del modelo a utilizar.
            messages (list): Lista de mensajes para la conversación.
            temperature (float): Temperatura para la generación.
            max_tokens (int): Número máximo de tokens en la respuesta.
            callback (callable, optional): Función de callback para cada fragmento de respuesta.
            
        Returns:
            str: Respuesta completa generada.
        """
        if not self.is_configured():
            return "Error: API no configurada. Por favor, proporciona una clave API."
        
        try:
            if self.logger:
                self.logger.info(f"Iniciando llamada a API (streaming) con modelo: {model}")
                self.logger.info(f"Parámetros: temperatura={temperature}, max_tokens={max_tokens}")
            
            start_time = time.time()
            
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            if self.logger:
                self.logger.info("Conexión establecida, comenzando streaming...")
            
            full_response = ""
            chunk_count = 0
            
            for chunk in stream:
                chunk_count += 1
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    
                    if callback:
                        callback(full_response)
            
            elapsed_time = time.time() - start_time
            
            if self.logger:
                self.logger.info(f"Streaming completado: {chunk_count} chunks recibidos en {elapsed_time:.2f} segundos")
            
            return full_response
        except Exception as e:
            error_msg = f"Error al llamar a la API: {str(e)}"
            
            if self.logger:
                self.logger.error(error_msg)
                self.logger.exception("Detalles del error:")
            
            return error_msg
