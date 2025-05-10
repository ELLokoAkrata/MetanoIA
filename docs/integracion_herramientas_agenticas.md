# Guía de Integración de Herramientas Agénticas en MetanoIA

Este documento describe el proceso estructurado para integrar las herramientas agénticas de Groq en MetanoIA, permitiendo funcionalidades como búsqueda web en tiempo real y ejecución de código, y cómo incorporar esta información al contexto de la conversación.

## Introducción a las Herramientas Agénticas de Groq

Groq ofrece dos sistemas de herramientas agénticas que permiten a los modelos interactuar con el mundo exterior:

1. **compound-beta**: Soporta múltiples llamadas a herramientas por solicitud. Ideal para casos que requieren varias búsquedas web o ejecuciones de código.
2. **compound-beta-mini**: Soporta una única llamada a herramienta por solicitud. Tiene una latencia aproximadamente 3 veces menor que compound-beta.

Ambos sistemas incluyen las siguientes herramientas:
- **Búsqueda Web** a través de [Tavily](https://tavily.com/)
- **Ejecución de Código** a través de [E2B](https://e2b.dev/) (actualmente solo soporta Python)

## Arquitectura de Integración

Para integrar estas herramientas en MetanoIA, seguiremos una arquitectura modular que permita:

1. Seleccionar modelos agénticos (compound-beta o compound-beta-mini)
2. Capturar y mostrar los resultados de las herramientas
3. Incorporar la información obtenida al contexto de la conversación
4. Configurar parámetros de búsqueda

## Proceso de Integración

### 1. Actualizar la Configuración de Modelos

Primero, debemos actualizar el archivo de configuración de modelos para incluir los modelos agénticos:

```python
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
```

### 2. Actualizar el Cliente de Groq

Modificar el cliente de Groq para capturar y procesar los resultados de las herramientas agénticas:

```python
def generate_streaming_response(self, model, messages, temperature, max_tokens, callback=None):
    """
    Genera una respuesta en streaming.
    
    Args:
        model (str): ID del modelo.
        messages (list): Lista de mensajes.
        temperature (float): Temperatura para la generación.
        max_tokens (int): Número máximo de tokens a generar.
        callback (function, optional): Función de callback para actualizar la respuesta.
        
    Returns:
        dict: Respuesta completa generada, incluyendo el contenido y las herramientas ejecutadas.
    """
    # Verificar si el cliente está configurado
    if not self.is_configured():
        logger.error("Cliente de Groq no configurado. Establezca una API key válida.")
        return {"content": "Error: Cliente de Groq no configurado. Por favor, proporcione una API key válida."}
    
    # Verificar si hay una respuesta cacheada
    cache_key = f"{model}_{str(messages)}_{temperature}_{max_tokens}"
    cached_response = self.response_cache.get(cache_key)
    if cached_response:
        logger.info(f"Usando respuesta cacheada para {model}")
        if callback:
            callback(cached_response["content"])
        return cached_response
    
    try:
        # Crear la solicitud de completado
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        # Procesar la respuesta en streaming
        response_text = ""
        executed_tools = []
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response_text += content
                if callback:
                    callback(response_text)
            
            # Capturar herramientas ejecutadas si están disponibles
            if hasattr(chunk.choices[0].delta, 'executed_tools'):
                if chunk.choices[0].delta.executed_tools:
                    executed_tools.extend(chunk.choices[0].delta.executed_tools)
        
        # Guardar en caché
        result = {
            "content": response_text,
            "executed_tools": executed_tools
        }
        self.response_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        error_msg = f"Error al generar respuesta con Groq: {str(e)}"
        logger.error(error_msg)
        return {"content": f"Error: {error_msg}"}
```

### 3. Crear un Gestor de Contexto para Herramientas Agénticas

Implementar un nuevo módulo para gestionar el contexto de las herramientas agénticas:

```python
"""
Módulo para la gestión del contexto de herramientas agénticas.
"""
import streamlit as st
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
    
    def add_search_result(self, search_result):
        """
        Añade un resultado de búsqueda al contexto.
        
        Args:
            search_result (dict): Resultado de búsqueda a añadir.
        """
        self.session_state.agentic_context["search_results"].append(search_result)
        logger.info(f"Añadido resultado de búsqueda al contexto: {search_result['title']}")
    
    def add_code_execution(self, code_execution):
        """
        Añade una ejecución de código al contexto.
        
        Args:
            code_execution (dict): Ejecución de código a añadir.
        """
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
            tool_type = tool.get("type")
            
            if tool_type == "search":
                # Procesar resultado de búsqueda
                search_result = {
                    "query": tool.get("input", {}).get("query", ""),
                    "timestamp": tool.get("timestamp"),
                    "results": tool.get("output", {}).get("results", []),
                    "title": f"Búsqueda: {tool.get('input', {}).get('query', '')}"
                }
                self.add_search_result(search_result)
            
            elif tool_type == "code_execution":
                # Procesar ejecución de código
                code_execution = {
                    "code": tool.get("input", {}).get("code", ""),
                    "timestamp": tool.get("timestamp"),
                    "result": tool.get("output", {}).get("result", ""),
                    "error": tool.get("output", {}).get("error", "")
                }
                self.add_code_execution(code_execution)
    
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
```

### 4. Actualizar la Interfaz de Usuario

Modificar la barra lateral para incluir opciones de configuración de herramientas agénticas:

```python
def render_agentic_tools_config(session_state, agentic_tools_manager):
    """
    Renderiza la configuración de herramientas agénticas en la barra lateral.
    
    Args:
        session_state: Estado de la sesión de Streamlit.
        agentic_tools_manager: Gestor de herramientas agénticas.
    """
    st.sidebar.markdown("## Herramientas Agénticas")
    
    # Activar/desactivar herramientas agénticas
    enable_agentic = st.sidebar.checkbox(
        "Activar herramientas agénticas",
        value=session_state.context.get("enable_agentic", False),
        key="enable_agentic"
    )
    
    if enable_agentic:
        # Configuración de búsqueda
        st.sidebar.markdown("### Configuración de Búsqueda")
        
        search_depth = st.sidebar.selectbox(
            "Profundidad de búsqueda",
            options=["basic", "advanced"],
            index=0 if session_state.agentic_context["search_settings"]["search_depth"] == "basic" else 1,
            key="search_depth"
        )
        
        max_results = st.sidebar.slider(
            "Máximo de resultados",
            min_value=1,
            max_value=10,
            value=session_state.agentic_context["search_settings"]["max_results"],
            key="max_results"
        )
        
        include_domains = st.sidebar.text_input(
            "Dominios a incluir (separados por comas)",
            value=",".join(session_state.agentic_context["search_settings"]["include_domains"]),
            key="include_domains"
        )
        
        exclude_domains = st.sidebar.text_input(
            "Dominios a excluir (separados por comas)",
            value=",".join(session_state.agentic_context["search_settings"]["exclude_domains"]),
            key="exclude_domains"
        )
        
        # Actualizar configuración
        agentic_tools_manager.update_search_settings({
            "search_depth": search_depth,
            "max_results": max_results,
            "include_domains": [domain.strip() for domain in include_domains.split(",") if domain.strip()],
            "exclude_domains": [domain.strip() for domain in exclude_domains.split(",") if domain.strip()]
        })
    
    # Actualizar el contexto
    session_state.context["enable_agentic"] = enable_agentic
```

### 5. Actualizar el Componente de Chat

Modificar el componente de chat para mostrar los resultados de las herramientas agénticas:

```python
def display_agentic_context(session_state, agentic_tools_manager):
    """
    Muestra el contexto de herramientas agénticas en la interfaz.
    
    Args:
        session_state: Estado de la sesión de Streamlit.
        agentic_tools_manager: Gestor de herramientas agénticas.
    """
    if not session_state.context.get("enable_agentic", False):
        return
    
    context = agentic_tools_manager.get_context_for_display()
    
    # Mostrar resultados de búsqueda
    if context["search_results"]:
        with st.expander("Resultados de búsqueda", expanded=False):
            for i, result in enumerate(context["search_results"]):
                st.markdown(f"### Búsqueda {i+1}: {result['query']}")
                for item in result['results']:
                    st.markdown(f"**{item.get('title', 'Sin título')}**")
                    st.markdown(f"{item.get('content', 'Sin contenido')}")
                    st.markdown(f"Fuente: [{item.get('url', 'Desconocida')}]({item.get('url', '#')})")
                    st.markdown("---")
    
    # Mostrar ejecuciones de código
    if context["code_executions"]:
        with st.expander("Ejecuciones de código", expanded=False):
            for i, execution in enumerate(context["code_executions"]):
                st.markdown(f"### Ejecución {i+1}")
                st.code(execution['code'], language="python")
                st.markdown("**Resultado:**")
                if execution['error']:
                    st.error(execution['error'])
                else:
                    st.code(execution['result'])
                st.markdown("---")
```

### 6. Modificar el Procesamiento de Mensajes

Actualizar el procesamiento de mensajes para incluir el contexto de herramientas agénticas:

```python
def handle_user_input(prompt, session_state, groq_client, logger):
    """
    Procesa la entrada del usuario y genera una respuesta.
    
    Args:
        prompt (str): Mensaje del usuario.
        session_state: Estado de la sesión de Streamlit.
        groq_client: Cliente de Groq.
        logger: Logger para registrar eventos.
    """
    # Añadir mensaje del usuario
    session_state.messages.append({"role": "user", "content": prompt})
    
    # Obtener modelo actual
    current_model = session_state.context["model"]
    model_obj = get_model(current_model)
    
    # Verificar si es un modelo agéntico
    is_agentic_model = model_obj.is_agentic if hasattr(model_obj, "is_agentic") else False
    
    # Preparar mensajes para la API
    api_messages = []
    
    # Añadir system prompt
    api_messages.append({
        "role": "system",
        "content": session_state.context["system_prompt"]
    })
    
    # Añadir contexto de herramientas agénticas si está habilitado
    if session_state.context.get("enable_agentic", False) and is_agentic_model:
        agentic_tools_manager = AgenticToolsManager(session_state)
        agentic_context = agentic_tools_manager.get_context_for_model()
        
        if agentic_context:
            api_messages.append({
                "role": "system",
                "content": f"Contexto adicional de herramientas agénticas:\n\n{agentic_context}"
            })
    
    # Añadir mensajes de la conversación (limitados por el contexto del modelo)
    max_context = model_obj.max_context_messages if model_obj else 10
    for msg in session_state.messages[-max_context:]:
        api_messages.append(msg)
    
    # Mostrar mensaje de "Pensando..."
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Pensando...")
        
        # Función para actualizar la respuesta en tiempo real
        full_response = ""
        def update_response(text):
            nonlocal full_response
            full_response = text
            message_placeholder.markdown(text + "▌")
        
        # Generar respuesta
        response = groq_client.generate_streaming_response(
            model=current_model,
            messages=api_messages,
            temperature=session_state.context["temperature"],
            max_tokens=session_state.context["max_tokens"],
            callback=update_response
        )
        
        # Mostrar respuesta final
        if isinstance(response, dict):
            content = response.get("content", "")
            executed_tools = response.get("executed_tools", [])
            
            # Procesar herramientas ejecutadas
            if session_state.context.get("enable_agentic", False) and is_agentic_model:
                agentic_tools_manager = AgenticToolsManager(session_state)
                agentic_tools_manager.process_executed_tools(executed_tools)
            
            message_placeholder.markdown(content)
            session_state.messages.append({"role": "assistant", "content": content})
        else:
            message_placeholder.markdown(response)
            session_state.messages.append({"role": "assistant", "content": response})
```

### 7. Actualizar el Archivo Principal

Modificar `app.py` para inicializar el gestor de herramientas agénticas:

```python
def main():
    """Función principal de la aplicación."""
    # Configurar el logger
    logger = setup_logger("MetanoIA")
    
    # Aplicar el tema personalizado
    apply_fresh_tech_theme()
    
    # Inicializar el estado de la sesión
    session_state = initialize_session_state()
    
    # Inicializar el cliente de Groq
    groq_client = GroqClient(logger=logger)
    
    # Inicializar el gestor de herramientas agénticas
    agentic_tools_manager = AgenticToolsManager(session_state)
    
    # Título principal
    st.title("🤖 MetanoIA")
    st.markdown("Chat bot modular usando Streamlit y la API de Groq")
    
    # Renderizar la barra lateral
    config_changed = render_sidebar(session_state, groq_client, logger)
    
    # Renderizar configuración de herramientas agénticas
    render_agentic_tools_config(session_state, agentic_tools_manager)
    
    # Si la configuración cambió, recargar la página
    if config_changed:
        st.rerun()
    
    # Contenedor principal del chat
    chat_container = st.container()
    
    # Mostrar mensajes anteriores
    with chat_container:
        display_chat_history(session_state, AVAILABLE_MODELS)
        display_agentic_context(session_state, agentic_tools_manager)
    
    # Entrada de usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        handle_user_input(prompt, session_state, groq_client, logger)
```

## Flujo de Trabajo para Integrar Herramientas Agénticas

A continuación se describe el flujo de trabajo completo para integrar y utilizar herramientas agénticas en MetanoIA:

1. **Selección de Modelo Agéntico**:
   - El usuario selecciona un modelo agéntico (compound-beta o compound-beta-mini) en la interfaz.
   - Se activa la opción "Activar herramientas agénticas" en la barra lateral.

2. **Configuración de Búsqueda**:
   - El usuario configura los parámetros de búsqueda:
     - Profundidad de búsqueda (básica o avanzada)
     - Número máximo de resultados
     - Dominios a incluir o excluir

3. **Interacción con el Modelo**:
   - El usuario envía un mensaje que puede requerir búsqueda web o ejecución de código.
   - El modelo decide automáticamente si utilizar las herramientas agénticas.

4. **Procesamiento de Resultados**:
   - Las herramientas ejecutadas se capturan en la respuesta de la API.
   - El gestor de herramientas agénticas procesa estos resultados y los añade al contexto.

5. **Visualización de Resultados**:
   - Los resultados de búsqueda y ejecuciones de código se muestran en la interfaz.
   - El usuario puede expandir estos resultados para obtener más información.

6. **Incorporación al Contexto**:
   - La información obtenida se incorpora al contexto de la conversación.
   - En futuras interacciones, el modelo tiene acceso a esta información.

## Consideraciones Importantes

### Limitaciones

- Las herramientas agénticas solo están disponibles con los modelos compound-beta y compound-beta-mini.
- La ejecución de código solo soporta Python actualmente.
- El contexto de herramientas agénticas consume tokens del límite de contexto del modelo.

### Seguridad

- La ejecución de código se realiza en un entorno aislado proporcionado por E2B.
- Los resultados de búsqueda web pueden contener información desactualizada o incorrecta.

### Rendimiento

- compound-beta-mini tiene una latencia aproximadamente 3 veces menor que compound-beta.
- El uso de herramientas agénticas aumenta el tiempo de respuesta debido a las llamadas a servicios externos.

## Ejemplos de Uso

### Ejemplo 1: Búsqueda Web

```python
# Configuración
session_state.context["model"] = "compound-beta"
session_state.context["enable_agentic"] = True
session_state.agentic_context["search_settings"]["search_depth"] = "basic"
session_state.agentic_context["search_settings"]["max_results"] = 3

# Mensaje del usuario
prompt = "¿Cuáles son las últimas noticias sobre inteligencia artificial?"
```

### Ejemplo 2: Ejecución de Código

```python
# Configuración
session_state.context["model"] = "compound-beta"
session_state.context["enable_agentic"] = True

# Mensaje del usuario
prompt = "Crea un gráfico de barras con matplotlib que muestre las ventas mensuales de 2023"
```

## Conclusión

La integración de herramientas agénticas en MetanoIA permite ampliar significativamente las capacidades de la aplicación, permitiendo a los modelos acceder a información en tiempo real y ejecutar código. Esta funcionalidad mejora la experiencia del usuario al proporcionar respuestas más precisas y actualizadas, y al permitir la ejecución de tareas complejas directamente desde la interfaz de chat.

La arquitectura modular de MetanoIA facilita esta integración, manteniendo la coherencia con el diseño existente y permitiendo futuras extensiones a medida que Groq añada nuevas herramientas agénticas.

**Estado**: ✅ Implementado