"""
Módulo para la gestión de variables de entorno.
"""
import os
from dotenv import load_dotenv

def load_environment_variables():
    """
    Carga las variables de entorno desde un archivo .env si existe.
    
    Returns:
        dict: Diccionario con las variables de entorno cargadas.
    """
    # Intentar cargar desde .env si existe
    load_dotenv()
    
    # Variables de entorno relevantes para la aplicación
    env_vars = {
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY"),
        # Agregar otras variables de entorno según sea necesario
    }
    
    return env_vars
