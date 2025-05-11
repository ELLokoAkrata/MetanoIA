"""
Módulo que define las implementaciones concretas de los modelos de Groq.
"""
from src.models.base_model import BaseLanguageModel

class DeepSeekModel(BaseLanguageModel):
    """Implementación del modelo DeepSeek de Groq."""
    
    @property
    def id(self):
        return "deepseek-r1-distill-llama-70b"
    
    @property
    def display_name(self):
        return "DeepSeek (128K)"
    
    @property
    def context_length(self):
        return 128000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Groq"

class MetaMaverickModel(BaseLanguageModel):
    """Implementación del modelo Meta Llama 4 Maverick de Groq.
    Este modelo soporta capacidades de visión para procesar imágenes."""
    
    @property
    def id(self):
        return "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    @property
    def display_name(self):
        return "Meta Maverick (131K)"
    
    @property
    def context_length(self):
        return 131072
    
    @property
    def max_context_messages(self):
        return 5  # Limitado debido a restricciones de TPM
    
    @property
    def provider(self):
        return "Groq"
        
    @property
    def supports_vision(self):
        return True

class MetaScoutModel(BaseLanguageModel):
    """Implementación del modelo Meta Llama 4 Scout de Groq.
    Este modelo soporta capacidades de visión para procesar imágenes."""
    
    @property
    def id(self):
        return "meta-llama/llama-4-scout-17b-16e-instruct"
    
    @property
    def display_name(self):
        return "Meta Scout (131K)"
    
    @property
    def context_length(self):
        return 131072
    
    @property
    def max_context_messages(self):
        return 6  # Limitado debido a restricciones de TPM
    
    @property
    def provider(self):
        return "Groq"
        
    @property
    def supports_vision(self):
        return True

class QwenModel(BaseLanguageModel):
    """Implementación del modelo Qwen de Groq."""
    
    @property
    def id(self):
        return "qwen-qwq-32b"
    
    @property
    def display_name(self):
        return "Alibaba Qwen (128K)"
    
    @property
    def context_length(self):
        return 128000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Groq"

# Diccionario de todos los modelos disponibles
AVAILABLE_MODELS = {
    model.id: model for model in [
        DeepSeekModel(),
        MetaMaverickModel(),
        MetaScoutModel(),
        QwenModel()
    ]
}

def get_model(model_id):
    """
    Obtiene una instancia del modelo por su ID.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        BaseLanguageModel: Instancia del modelo o None si no se encuentra.
    """
    return AVAILABLE_MODELS.get(model_id)

def get_all_models():
    """
    Obtiene todos los modelos disponibles.
    
    Returns:
        dict: Diccionario de modelos disponibles.
    """
    return AVAILABLE_MODELS
