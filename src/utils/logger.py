"""
Módulo para la configuración del sistema de logging.
"""
import logging

def setup_logger(name="MetanoIA"):
    """
    Configura y devuelve un logger con el formato y nivel especificados.
    
    Args:
        name (str): Nombre del logger.
        
    Returns:
        logging.Logger: Instancia del logger configurado.
    """
    # Configurar sistema de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(name)
