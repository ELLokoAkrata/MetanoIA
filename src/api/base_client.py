"""
Módulo que define la clase base para los clientes de API.
"""
from abc import ABC, abstractmethod

class BaseAPIClient(ABC):
    """
    Clase base abstracta para los clientes de API.
    Define la interfaz común que deben implementar todos los clientes.
    """
    
    @abstractmethod
    def is_configured(self):
        """
        Verifica si el cliente está configurado correctamente.
        
        Returns:
            bool: True si el cliente está configurado, False en caso contrario.
        """
        pass
    
    @abstractmethod
    def set_api_key(self, api_key):
        """
        Establece la clave API para el cliente.
        
        Args:
            api_key (str): Clave API para el servicio.
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
