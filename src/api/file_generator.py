"""
Módulo para la generación de archivos utilizando herramientas (tools) de Groq.

Este módulo proporciona las definiciones de herramientas y funciones para generar
archivos en diferentes formatos (JSON, Python, Markdown y TXT) utilizando la API de Groq.
"""
import os
import json
import tempfile
from datetime import datetime
from typing import Dict, Any, List, Optional

class FileGenerator:
    """
    Clase para generar archivos en diferentes formatos utilizando herramientas de Groq.
    
    Esta clase proporciona las definiciones de herramientas y funciones para generar
    archivos en diferentes formatos (JSON, Python, Markdown y TXT).
    """
    
    def __init__(self, temp_dir: Optional[str] = None, logger=None):
        """
        Inicializa el generador de archivos.
        
        Args:
            temp_dir (str, optional): Directorio temporal para guardar los archivos generados.
                                     Si no se proporciona, se utilizará el directorio temporal del sistema.
            logger (logging.Logger, optional): Logger para registrar información.
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.logger = logger
        
        # Crear directorio temporal si no existe
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
        if self.logger:
            self.logger.info(f"FileGenerator inicializado con directorio temporal: {self.temp_dir}")
    
    def get_tools_definitions(self) -> List[Dict[str, Any]]:
        """
        Obtiene las definiciones de herramientas para la generación de archivos.
        
        Returns:
            List[Dict[str, Any]]: Lista de definiciones de herramientas.
        """
        return [
            # Herramienta para generar archivos JSON
            {
                "type": "function",
                "function": {
                    "name": "generate_json_file",
                    "description": "Genera un archivo JSON basado en la solicitud del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "object",
                                "description": "El contenido del archivo JSON"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Nombre del archivo a generar (sin extensión)"
                            }
                        },
                        "required": ["content", "filename"]
                    }
                }
            },
            # Herramienta para generar archivos Python
            {
                "type": "function",
                "function": {
                    "name": "generate_python_file",
                    "description": "Genera un archivo Python (.py) basado en la solicitud del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "El contenido del archivo Python (código)"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Nombre del archivo a generar (sin extensión)"
                            }
                        },
                        "required": ["content", "filename"]
                    }
                }
            },
            # Herramienta para generar archivos Markdown
            {
                "type": "function",
                "function": {
                    "name": "generate_markdown_file",
                    "description": "Genera un archivo Markdown (.md) basado en la solicitud del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "El contenido del archivo Markdown"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Nombre del archivo a generar (sin extensión)"
                            }
                        },
                        "required": ["content", "filename"]
                    }
                }
            },
            # Herramienta para generar archivos de texto
            {
                "type": "function",
                "function": {
                    "name": "generate_text_file",
                    "description": "Genera un archivo de texto (.txt) basado en la solicitud del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "El contenido del archivo de texto"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Nombre del archivo a generar (sin extensión)"
                            }
                        },
                        "required": ["content", "filename"]
                    }
                }
            }
        ]
    
    def get_available_functions(self) -> Dict[str, callable]:
        """
        Obtiene un diccionario con las funciones disponibles para las herramientas.
        
        Returns:
            Dict[str, callable]: Diccionario con las funciones disponibles.
        """
        return {
            "generate_json_file": self.generate_json_file,
            "generate_python_file": self.generate_python_file,
            "generate_markdown_file": self.generate_markdown_file,
            "generate_text_file": self.generate_text_file
        }
    
    def generate_json_file(self, content: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """
        Genera un archivo JSON y devuelve la información para su descarga.
        
        Args:
            content (Dict[str, Any]): Contenido del archivo JSON.
            filename (str): Nombre del archivo sin extensión.
            
        Returns:
            Dict[str, Any]: Información del archivo generado.
        """
        # Asegurar que el nombre del archivo sea seguro
        safe_filename = self._sanitize_filename(filename)
        
        # Añadir extensión si no la tiene
        if not safe_filename.endswith('.json'):
            safe_filename += '.json'
        
        # Crear ruta completa
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.temp_dir, f"{safe_filename}")
        
        try:
            # Guardar contenido en el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            if self.logger:
                self.logger.info(f"Archivo JSON generado: {file_path}")
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": "json",
                "file_name": os.path.basename(file_path),
                "message": f"Archivo JSON '{safe_filename}' generado correctamente."
            }
        except Exception as e:
            error_msg = f"Error al generar archivo JSON: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def generate_python_file(self, content: str, filename: str) -> Dict[str, Any]:
        """
        Genera un archivo Python y devuelve la información para su descarga.
        
        Args:
            content (str): Contenido del archivo Python (código).
            filename (str): Nombre del archivo sin extensión.
            
        Returns:
            Dict[str, Any]: Información del archivo generado.
        """
        # Asegurar que el nombre del archivo sea seguro
        safe_filename = self._sanitize_filename(filename)
        
        # Añadir extensión si no la tiene
        if not safe_filename.endswith('.py'):
            safe_filename += '.py'
        
        # Crear ruta completa
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.temp_dir, f"{safe_filename}")
        
        try:
            # Guardar contenido en el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.logger:
                self.logger.info(f"Archivo Python generado: {file_path}")
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": "python",
                "file_name": os.path.basename(file_path),
                "message": f"Archivo Python '{safe_filename}' generado correctamente."
            }
        except Exception as e:
            error_msg = f"Error al generar archivo Python: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def generate_markdown_file(self, content: str, filename: str) -> Dict[str, Any]:
        """
        Genera un archivo Markdown y devuelve la información para su descarga.
        
        Args:
            content (str): Contenido del archivo Markdown.
            filename (str): Nombre del archivo sin extensión.
            
        Returns:
            Dict[str, Any]: Información del archivo generado.
        """
        # Asegurar que el nombre del archivo sea seguro
        safe_filename = self._sanitize_filename(filename)
        
        # Añadir extensión si no la tiene
        if not safe_filename.endswith('.md'):
            safe_filename += '.md'
        
        # Crear ruta completa
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.temp_dir, f"{safe_filename}")
        
        try:
            # Guardar contenido en el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.logger:
                self.logger.info(f"Archivo Markdown generado: {file_path}")
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": "markdown",
                "file_name": os.path.basename(file_path),
                "message": f"Archivo Markdown '{safe_filename}' generado correctamente."
            }
        except Exception as e:
            error_msg = f"Error al generar archivo Markdown: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def generate_text_file(self, content: str, filename: str) -> Dict[str, Any]:
        """
        Genera un archivo de texto y devuelve la información para su descarga.
        
        Args:
            content (str): Contenido del archivo de texto.
            filename (str): Nombre del archivo sin extensión.
            
        Returns:
            Dict[str, Any]: Información del archivo generado.
        """
        # Asegurar que el nombre del archivo sea seguro
        safe_filename = self._sanitize_filename(filename)
        
        # Añadir extensión si no la tiene
        if not safe_filename.endswith('.txt'):
            safe_filename += '.txt'
        
        # Crear ruta completa
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(self.temp_dir, f"{safe_filename}")
        
        try:
            # Guardar contenido en el archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.logger:
                self.logger.info(f"Archivo de texto generado: {file_path}")
            
            return {
                "success": True,
                "file_path": file_path,
                "file_type": "text",
                "file_name": os.path.basename(file_path),
                "message": f"Archivo de texto '{safe_filename}' generado correctamente."
            }
        except Exception as e:
            error_msg = f"Error al generar archivo de texto: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitiza un nombre de archivo para evitar problemas de seguridad.
        
        Args:
            filename (str): Nombre de archivo a sanitizar.
            
        Returns:
            str: Nombre de archivo sanitizado.
        """
        # Eliminar caracteres no permitidos en nombres de archivo
        import re
        # Reemplazar caracteres no permitidos con guiones bajos
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', filename)
        # Eliminar espacios al inicio y final
        safe_name = safe_name.strip()
        # Si está vacío, usar un nombre predeterminado
        if not safe_name:
            safe_name = f"archivo_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return safe_name
