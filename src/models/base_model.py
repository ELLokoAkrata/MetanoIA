"""
Módulo que define la clase base para los modelos de lenguaje.
"""
from abc import ABC, abstractmethod

class BaseLanguageModel(ABC):
    """
    Clase base abstracta para los modelos de lenguaje.
    Define la interfaz común que deben implementar todos los modelos.
    """
    
    @property
    @abstractmethod
    def id(self):
        """
        Identificador único del modelo.
        
        Returns:
            str: ID del modelo.
        """
        pass
    
    @property
    @abstractmethod
    def display_name(self):
        """
        Nombre para mostrar del modelo.
        
        Returns:
            str: Nombre para mostrar.
        """
        pass
    
    @property
    @abstractmethod
    def context_length(self):
        """
        Longitud máxima de contexto que soporta el modelo.
        
        Returns:
            int: Número máximo de tokens de contexto.
        """
        pass
    
    @property
    @abstractmethod
    def max_context_messages(self):
        """
        Número máximo de mensajes recomendados para el contexto.
        
        Returns:
            int: Número máximo de mensajes.
        """
        pass
    
    @property
    @abstractmethod
    def provider(self):
        """
        Proveedor del modelo.
        
        Returns:
            str: Nombre del proveedor.
        """
        pass
    
    @property
    def supports_vision(self):
        """
        Indica si el modelo soporta capacidades de visión.
        
        Returns:
            bool: True si el modelo soporta visión, False en caso contrario.
        """
        return False
