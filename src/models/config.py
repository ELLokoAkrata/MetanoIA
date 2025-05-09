"""
Módulo para la configuración y gestión de modelos disponibles.
"""
from src.models.groq_models import get_all_models as get_groq_models, get_model as get_groq_model
from src.models.agentic_models import get_all_agentic_models

# Combinar todos los modelos disponibles
def get_all_models():
    """
    Obtiene todos los modelos disponibles combinando modelos regulares y agénticos.
    
    Returns:
        dict: Diccionario con todos los modelos disponibles.
    """
    all_models = {}
    
    # Añadir modelos de Groq
    all_models.update(get_groq_models())
    
    # Añadir modelos agénticos
    all_models.update(get_all_agentic_models())
    
    return all_models

# Función para obtener un modelo específico
def get_model(model_id):
    """
    Obtiene un modelo específico por su ID.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        BaseLanguageModel: Modelo encontrado o None si no existe.
    """
    # Buscar en modelos de Groq
    model = get_groq_model(model_id)
    if model:
        return model
    
    # Buscar en modelos agénticos
    agentic_models = get_all_agentic_models()
    return agentic_models.get(model_id)

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
