"""
Módulo que define los modelos agénticos de Groq disponibles.
"""
from src.models.base_model import BaseLanguageModel

class CompoundBetaModel(BaseLanguageModel):
    """
    Modelo Compound Beta de Groq con capacidades agénticas.
    """
    
    def __init__(self):
        """Inicializa el modelo Compound Beta."""
        self._id = "compound-beta"
        self._display_name = "Compound Beta (Agéntico)"
        self._description = "Modelo agéntico con múltiples llamadas a herramientas por solicitud"
    
    @property
    def id(self):
        return self._id
    
    @property
    def display_name(self):
        return self._display_name
    
    @property
    def description(self):
        return self._description
    
    @property
    def context_length(self):
        return 128000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Groq"
    
    @property
    def is_agentic(self):
        return True
    
    @property
    def supports_multiple_tools(self):
        return True


class CompoundBetaMiniModel(BaseLanguageModel):
    """
    Modelo Compound Beta Mini de Groq con capacidades agénticas.
    """
    
    def __init__(self):
        """Inicializa el modelo Compound Beta Mini."""
        self._id = "compound-beta-mini"
        self._display_name = "Compound Beta Mini (Agéntico)"
        self._description = "Modelo agéntico con una llamada a herramienta por solicitud (menor latencia)"
    
    @property
    def id(self):
        return self._id
    
    @property
    def display_name(self):
        return self._display_name
    
    @property
    def description(self):
        return self._description
    
    @property
    def context_length(self):
        return 128000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Groq"
    
    @property
    def is_agentic(self):
        return True
    
    @property
    def supports_multiple_tools(self):
        return False


def get_all_agentic_models():
    """
    Obtiene todos los modelos agénticos disponibles.
    
    Returns:
        dict: Diccionario con los modelos agénticos disponibles.
    """
    models = [
        CompoundBetaModel(),
        CompoundBetaMiniModel()
    ]
    
    return {model.id: model for model in models}
