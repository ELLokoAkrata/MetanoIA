"""
Módulo para la gestión del contexto de herramientas agénticas.
"""
import streamlit as st
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger("AgenticTools")

class AgenticToolsManager:
    """
    Gestor de herramientas agénticas y su contexto.
    """
    
    def __init__(self, session_state):
        """
        Inicializa el gestor de herramientas agénticas.
        
        Args:
            session_state: Estado de la sesión de Streamlit.
        """
        self.session_state = session_state
        self._initialize_agentic_context()
    
    def _initialize_agentic_context(self):
        """Inicializa el contexto de herramientas agénticas en la sesión."""
        if "agentic_context" not in self.session_state:
            self.session_state.agentic_context = {
                "search_results": [],
                "code_executions": [],
                "search_settings": {
                    "search_depth": "basic",  # basic, advanced
                    "include_domains": [],
                    "exclude_domains": [],
                    "max_results": 3
                }
            }
    
    def update_search_settings(self, settings):
        """
        Actualiza la configuración de búsqueda.
        
        Args:
            settings (dict): Nueva configuración de búsqueda.
        """
        self.session_state.agentic_context["search_settings"].update(settings)
        logger.info(f"Configuración de búsqueda actualizada: {settings}")
    
    def add_search_result(self, search_result):
        """
        Añade un resultado de búsqueda al contexto.
        
        Args:
            search_result (dict): Resultado de búsqueda a añadir.
        """
        # Añadir timestamp si no existe
        if "timestamp" not in search_result:
            search_result["timestamp"] = datetime.now().isoformat()
        
        # Añadir título si no existe
        if "title" not in search_result and "query" in search_result:
            search_result["title"] = f"Búsqueda: {search_result['query']}"
        
        self.session_state.agentic_context["search_results"].append(search_result)
        logger.info(f"Añadido resultado de búsqueda al contexto: {search_result.get('title', 'Sin título')}")
    
    def add_code_execution(self, code_execution):
        """
        Añade una ejecución de código al contexto.
        
        Args:
            code_execution (dict): Ejecución de código a añadir.
        """
        # Añadir timestamp si no existe
        if "timestamp" not in code_execution:
            code_execution["timestamp"] = datetime.now().isoformat()
        
        self.session_state.agentic_context["code_executions"].append(code_execution)
        logger.info(f"Añadida ejecución de código al contexto")
    
    def process_executed_tools(self, executed_tools):
        """
        Procesa las herramientas ejecutadas y las añade al contexto.
        
        Args:
            executed_tools (list): Lista de herramientas ejecutadas.
        """
        if not executed_tools:
            return
        
        for tool in executed_tools:
            try:
                # Verificar que tool sea un diccionario
                if not isinstance(tool, dict):
                    logger.warning(f"Herramienta no es un diccionario: {tool}")
                    continue
                
                tool_type = tool.get("type")
                
                # Obtener input y output de forma segura
                tool_input = tool.get("input", {})
                tool_output = tool.get("output", {})
                
                # Convertir a diccionario si son strings
                if isinstance(tool_input, str):
                    logger.warning(f"Input es un string: {tool_input}")
                    tool_input = {"raw": tool_input}
                
                if isinstance(tool_output, str):
                    logger.warning(f"Output es un string: {tool_output}")
                    tool_output = {"raw": tool_output}
                
                if tool_type == "search":
                    # Procesar resultado de búsqueda
                    search_result = {
                        "query": tool_input.get("query", ""),
                        "timestamp": tool.get("timestamp", datetime.now().isoformat()),
                        "results": tool_output.get("results", []),
                        "title": f"Búsqueda: {tool_input.get('query', '')}"
                    }
                    self.add_search_result(search_result)
                    logger.info(f"Procesado resultado de búsqueda: {search_result['query']}")
                
                elif tool_type == "code_execution":
                    # Procesar ejecución de código
                    code_execution = {
                        "code": tool_input.get("code", ""),
                        "timestamp": tool.get("timestamp", datetime.now().isoformat()),
                        "result": tool_output.get("result", ""),
                        "error": tool_output.get("error", "")
                    }
                    self.add_code_execution(code_execution)
                    logger.info(f"Procesada ejecución de código")
            except Exception as e:
                logger.error(f"Error al procesar herramienta: {str(e)}")
                logger.exception("Detalles del error:")
                continue
    
    def get_context_for_display(self):
        """
        Obtiene el contexto formateado para mostrar en la interfaz.
        
        Returns:
            dict: Contexto formateado.
        """
        return {
            "search_results": self.session_state.agentic_context["search_results"],
            "code_executions": self.session_state.agentic_context["code_executions"]
        }
    
    def get_context_for_model(self):
        """
        Obtiene el contexto formateado para enviar al modelo.
        
        Returns:
            str: Contexto formateado como texto.
        """
        context_text = ""
        
        # Añadir resultados de búsqueda
        if self.session_state.agentic_context["search_results"]:
            context_text += "## Información de búsquedas web:\n\n"
            for i, result in enumerate(self.session_state.agentic_context["search_results"][-3:]):
                context_text += f"### Búsqueda {i+1}: {result['query']}\n\n"
                for j, item in enumerate(result['results']):
                    context_text += f"- **{item.get('title', 'Sin título')}**\n"
                    context_text += f"  {item.get('content', 'Sin contenido')}\n"
                    context_text += f"  Fuente: {item.get('url', 'Desconocida')}\n\n"
        
        # Añadir ejecuciones de código
        if self.session_state.agentic_context["code_executions"]:
            context_text += "## Ejecuciones de código:\n\n"
            for i, execution in enumerate(self.session_state.agentic_context["code_executions"][-3:]):
                context_text += f"### Ejecución {i+1}:\n\n"
                context_text += f"```python\n{execution['code']}\n```\n\n"
                context_text += f"**Resultado:**\n\n"
                if execution['error']:
                    context_text += f"Error: {execution['error']}\n\n"
                else:
                    context_text += f"```\n{execution['result']}\n```\n\n"
        
        return context_text
    
    def clear_context(self):
        """
        Limpia el contexto de herramientas agénticas.
        """
        self.session_state.agentic_context["search_results"] = []
        self.session_state.agentic_context["code_executions"] = []
        logger.info("Contexto de herramientas agénticas limpiado")
