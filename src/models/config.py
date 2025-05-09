"""
Módulo para la configuración y gestión de modelos disponibles.
"""
from src.models.groq_models import get_all_models, get_model

# Obtener todos los modelos disponibles
AVAILABLE_MODELS = {model_id: model.display_name for model_id, model in get_all_models().items()}

def get_model_display_name(model_id):
    """
    Obtiene el nombre de visualización de un modelo.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        str: Nombre de visualización del modelo o el ID si no se encuentra.
    """
    model = get_model(model_id)
    return model.display_name if model else model_id

def get_context_limit(model_id):
    """
    Obtiene el límite de contexto para un modelo específico.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        int: Número máximo de mensajes para el contexto.
    """
    # Buscar coincidencias parciales para modelos que contengan ciertos patrones
    if "llama-4-maverick" in model_id:
        maverick_model = get_model("meta-llama/llama-4-maverick-17b-128e-instruct")
        return maverick_model.max_context_messages if maverick_model else 5
    elif "llama-4-scout" in model_id:
        scout_model = get_model("meta-llama/llama-4-scout-17b-16e-instruct")
        return scout_model.max_context_messages if scout_model else 6
    
    # Buscar coincidencia exacta
    model = get_model(model_id)
    return model.max_context_messages if model else 10  # Valor predeterminado
