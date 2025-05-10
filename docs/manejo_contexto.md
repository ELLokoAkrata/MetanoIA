# Manejo de Contexto en MetanoIA

Este documento explica cómo MetanoIA logra mantener el contexto de la conversación y la información obtenida a través de herramientas agénticas (como búsquedas web o ejecuciones de código) independientemente del modelo de lenguaje que se esté utilizando.

## Arquitectura de Gestión de Contexto

MetanoIA implementa un sistema de gestión de contexto que funciona de manera independiente al modelo de lenguaje utilizado, permitiendo que la información obtenida a través de herramientas como búsquedas web o ejecuciones de código se mantenga disponible incluso al cambiar entre diferentes modelos.

### Componentes Clave

1. **Estado de Sesión (Session State)**
   - Streamlit proporciona un mecanismo de estado de sesión (`st.session_state`) que persiste entre interacciones.
   - MetanoIA utiliza este estado para almacenar:
     - Historial de mensajes (`messages`)
     - Configuración del modelo actual (`context`)
     - Contexto de herramientas agénticas (`agentic_context`)

2. **Gestor de Herramientas Agénticas (`AgenticToolsManager`)**
   - Clase dedicada a gestionar el contexto de herramientas agénticas.
   - Almacena y formatea la información obtenida de búsquedas web y ejecuciones de código.
   - Proporciona métodos para obtener el contexto en diferentes formatos (para visualización y para enviar al modelo).

3. **Cliente API Abstracto (`BaseAPIClient`)**
   - Define una interfaz común para todos los clientes de API.
   - Permite cambiar fácilmente entre diferentes proveedores de modelos manteniendo la misma estructura.

4. **Implementaciones Específicas de Clientes (ej. `GroqClient`)**
   - Implementan la interfaz `BaseAPIClient` para proveedores específicos.
   - Gestionan la comunicación con la API del proveedor.
   - Procesan las respuestas, incluyendo las herramientas ejecutadas por modelos agénticos.

## Flujo de Trabajo del Contexto

### 1. Inicialización del Contexto

```python
# En src/utils/session_state.py
def initialize_session_state():
    """Inicializa el estado de la sesión."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "context" not in st.session_state:
        st.session_state.context = {
            "model": "modelo_predeterminado",
            "temperature": 0.7,
            "max_tokens": 1024,
            "system_prompt": "Prompt predeterminado",
            "enable_agentic": False
        }
    
    return st.session_state
```

### 2. Procesamiento de Entrada del Usuario

Cuando el usuario envía un mensaje:

1. Se agrega el mensaje al historial (`session_state.messages`).
2. Se preparan los mensajes para la API, incluyendo el sistema prompt y el historial reciente.
3. Si las herramientas agénticas están habilitadas, se inicializa el gestor de herramientas.
4. Se envía la solicitud al modelo a través del cliente API.

```python
# En src/components/chat.py
def handle_user_input(prompt, session_state, groq_client, logger):
    # Agregar mensaje del usuario al historial
    session_state.messages.append({"role": "user", "content": prompt})
    
    # Preparar mensajes para la API
    api_messages = prepare_api_messages(session_state, current_model, logger)
    
    # Inicializar el gestor de herramientas agénticas si está habilitado
    agentic_tools_manager = None
    if session_state.context.get("enable_agentic", False):
        agentic_tools_manager = AgenticToolsManager(session_state)
    
    # Generar respuesta
    response = groq_client.generate_streaming_response(
        model=current_model,
        messages=api_messages,
        temperature=session_state.context["temperature"],
        max_tokens=session_state.context["max_tokens"],
        callback=update_response
    )
```

### 3. Procesamiento de Herramientas Ejecutadas

Cuando un modelo agéntico ejecuta herramientas (como búsquedas web):

1. El cliente API recibe la información de las herramientas ejecutadas.
2. El gestor de herramientas agénticas procesa esta información y la almacena en el estado de la sesión.
3. La información queda disponible para futuros mensajes, independientemente del modelo que se use.

```python
# En src/components/chat.py
if isinstance(response, dict):
    content = response.get("content", "")
    executed_tools = response.get("executed_tools", [])
    
    # Procesar herramientas ejecutadas si hay un gestor de herramientas agénticas
    if agentic_tools_manager and executed_tools:
        logger.info(f"Procesando {len(executed_tools)} herramientas ejecutadas")
        agentic_tools_manager.process_executed_tools(executed_tools)
    
    # Agregar respuesta al historial con información del modelo usado y herramientas ejecutadas
    session_state.messages.append({
        "role": "assistant", 
        "content": content, 
        "model_used": current_model,
        "executed_tools": executed_tools
    })
```

### 4. Preparación de Mensajes para la API

Al preparar los mensajes para enviar a la API, se incluye el contexto de herramientas agénticas:

```python
# En src/components/chat.py
def prepare_api_messages(session_state, current_model, logger):
    api_messages = [
        {"role": "system", "content": session_state.context["system_prompt"]}
    ]
    
    # Limitar el número de mensajes según el modelo
    max_context_messages = get_context_limit(current_model)
    recent_messages = session_state.messages[-max_context_messages:] if len(session_state.messages) > max_context_messages else session_state.messages
    
    # Añadir contexto de herramientas agénticas si está habilitado
    if session_state.context.get("enable_agentic", False) and "agentic_context" in session_state:
        agentic_tools_manager = AgenticToolsManager(session_state)
        agentic_context = agentic_tools_manager.get_context_for_model()
        
        if agentic_context:
            # Añadir el contexto agéntico al prompt del sistema
            api_messages[0]["content"] += "\n\n### Contexto adicional:\n" + agentic_context
    
    # Añadir mensajes del historial
    for msg in recent_messages:
        if msg["role"] in ["user", "assistant"]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    return api_messages
```

## Independencia del Modelo

El sistema está diseñado para ser independiente del modelo utilizado:

1. **Abstracción del Cliente API**: La interfaz `BaseAPIClient` permite cambiar entre diferentes proveedores sin afectar el funcionamiento del sistema.

2. **Almacenamiento Centralizado**: Toda la información se almacena en el estado de la sesión de Streamlit, que es independiente del modelo.

3. **Procesamiento Uniforme**: Las herramientas ejecutadas se procesan de manera uniforme, independientemente del modelo que las haya ejecutado.

4. **Adaptación Automática**: El sistema adapta automáticamente el contexto según las capacidades del modelo (por ejemplo, limitando el número de mensajes para modelos con ventanas de contexto más pequeñas).

## Ventajas del Enfoque

1. **Persistencia del Conocimiento**: La información obtenida a través de herramientas agénticas persiste entre cambios de modelo.

2. **Flexibilidad**: Los usuarios pueden cambiar entre diferentes modelos sin perder el contexto de la conversación.

3. **Extensibilidad**: El sistema puede ampliarse fácilmente para soportar nuevos proveedores de modelos o nuevas herramientas agénticas.

4. **Optimización de Recursos**: El sistema adapta automáticamente el contexto según las capacidades del modelo, evitando exceder los límites de tokens.

## Conclusión

El sistema de gestión de contexto de MetanoIA permite mantener la continuidad de la conversación y la información obtenida a través de herramientas agénticas, independientemente del modelo de lenguaje utilizado. Esta arquitectura facilita la experimentación con diferentes modelos y proporciona una experiencia de usuario coherente y enriquecida.
