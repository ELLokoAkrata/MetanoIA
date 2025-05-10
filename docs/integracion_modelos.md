# Guía de Integración de Modelos en MetanoIA

Este documento explica paso a paso cómo funciona el sistema de cambio de modelos en MetanoIA y cómo implementar correctamente la integración de nuevos modelos para garantizar una experiencia fluida y sin errores.

## Índice

1. [Arquitectura del Sistema de Modelos](#arquitectura-del-sistema-de-modelos)
2. [Problemas Comunes y Soluciones](#problemas-comunes-y-soluciones)
3. [Implementación Paso a Paso](#implementación-paso-a-paso)
4. [Buenas Prácticas](#buenas-prácticas)
5. [Ejemplos de Integración](#ejemplos-de-integración)

## Arquitectura del Sistema de Modelos

MetanoIA utiliza una arquitectura modular para gestionar diferentes modelos de lenguaje. Esta arquitectura se compone de:

### 1. Configuración de Modelos

La configuración de modelos se maneja en el directorio `src/models/`:

- `config.py`: Define funciones para obtener y gestionar modelos disponibles
- `groq_models.py`: Implementa modelos específicos de Groq
- `agentic_models.py`: Implementa modelos con capacidades agénticas

### 2. Clientes API

Los clientes API se encuentran en el directorio `src/api/`:

- `base_client.py`: Define la interfaz común para todos los clientes
- `groq_client.py`: Implementa el cliente específico para la API de Groq

### 3. Componentes de Interfaz

Los componentes de interfaz que manejan la selección y cambio de modelos:

- `src/components/sidebar.py`: Gestiona la selección de modelos
- `src/components/chat.py`: Maneja la generación de respuestas con el modelo seleccionado

## Problemas Comunes y Soluciones

### Problema 1: Inconsistencia en el Cambio de Modelo

**Problema**: Al cambiar de modelo en la interfaz, a veces el cambio no se aplica realmente y se sigue utilizando el modelo anterior.

**Causas**:
1. **Estado persistente de Streamlit**: Streamlit mantiene el estado de los widgets entre recargas.
2. **Falta de reinicio completo**: No se fuerza un reinicio de la aplicación al cambiar de modelo.
3. **Falta de verificación explícita**: No se verifica qué modelo se está utilizando realmente.
4. **Falta de feedback visual**: No hay indicadores claros del modelo activo.

**Solución**:
1. **Usar key dinámica para widgets**: Forzar la recreación de widgets cuando cambia el modelo.
2. **Forzar reinicio de la aplicación**: Llamar a `st.rerun()` cuando cambia el modelo.
3. **Verificar el modelo antes de cada generación**: Comprobar explícitamente qué modelo se está usando.
4. **Añadir indicadores visuales**: Mostrar claramente qué modelo está activo.

## Implementación Paso a Paso

### Paso 1: Definir el Nuevo Modelo

Para añadir un nuevo modelo, primero debes definirlo en el archivo correspondiente según su tipo:

#### Para modelos estándar (sin capacidades agénticas):

```python
# En src/models/groq_models.py o un nuevo archivo para otro proveedor

class NuevoModeloProveedor:
    """Clase para el nuevo modelo."""
    
    def __init__(self):
        self.id = "proveedor/nuevo-modelo"
        self.display_name = "Nombre Amigable del Modelo"
        self.max_context_messages = 10  # Ajustar según las capacidades del modelo
        self.is_agentic = False  # False para modelos estándar
        
    # Otros métodos específicos del modelo si son necesarios

def get_all_models():
    """Obtiene todos los modelos disponibles de este proveedor."""
    models = {}
    
    # Añadir modelos existentes...
    
    # Añadir el nuevo modelo
    nuevo_modelo = NuevoModeloProveedor()
    models[nuevo_modelo.id] = nuevo_modelo
    
    return models
```

#### Para modelos agénticos:

```python
# En src/models/agentic_models.py

class NuevoModeloAgentico:
    """Clase para el nuevo modelo agéntico."""
    
    def __init__(self):
        self.id = "proveedor/nuevo-modelo-agentico"
        self.display_name = "Nombre Amigable del Modelo Agéntico"
        self.max_context_messages = 8  # Ajustar según las capacidades del modelo
        self.is_agentic = True  # True para modelos agénticos
        
    # Métodos específicos para capacidades agénticas
    
# Actualizar la función get_all_agentic_models para incluir el nuevo modelo
```

### Paso 2: Implementar el Cliente API (si es necesario)

Si el nuevo modelo utiliza un proveedor de API diferente, debes implementar un nuevo cliente:

```python
# En src/api/nuevo_proveedor_client.py

from src.api.base_client import BaseAPIClient

class NuevoProveedorClient(BaseAPIClient):
    """Cliente para interactuar con la API del nuevo proveedor."""
    
    def __init__(self, api_key=None, logger=None):
        """Inicializa el cliente."""
        self.api_key = api_key
        self.logger = logger
        self.client = None
        
        if self.api_key:
            # Inicializar el cliente con la API key
            self.client = NuevoProveedorSDK(api_key=self.api_key)
    
    def is_configured(self):
        """Verifica si el cliente está configurado correctamente."""
        return self.client is not None and self.api_key is not None
    
    def set_api_key(self, api_key):
        """Establece la clave API y reconfigura el cliente."""
        # Implementación...
    
    def get_cached_response(self, model, messages, temperature, max_tokens):
        """Obtiene una respuesta cacheada."""
        # Implementación...
    
    def generate_streaming_response(self, model, messages, temperature, max_tokens, callback=None):
        """Genera una respuesta en streaming."""
        # Implementación...
```

### Paso 3: Actualizar la Configuración Central

Actualiza `src/models/config.py` para incluir los nuevos modelos:

```python
# En src/models/config.py

# Importar el nuevo módulo de modelos si es necesario
from src.models.nuevo_proveedor_models import get_all_models as get_nuevo_proveedor_models
from src.models.nuevo_proveedor_models import get_model as get_nuevo_proveedor_model

def get_all_models():
    """Obtiene todos los modelos disponibles combinando modelos regulares y agénticos."""
    all_models = {}
    
    # Añadir modelos existentes
    all_models.update(get_groq_models())
    all_models.update(get_all_agentic_models())
    
    # Añadir nuevos modelos
    all_models.update(get_nuevo_proveedor_models())
    
    return all_models

def get_model(model_id):
    """Obtiene un modelo específico por su ID."""
    # Buscar en modelos existentes...
    
    # Buscar en nuevos modelos
    model = get_nuevo_proveedor_model(model_id)
    if model:
        return model
    
    # Resto del código...
```

### Paso 4: Implementar la Selección de Modelo en la Interfaz

La parte crítica: asegurarse de que el cambio de modelo funcione correctamente en la interfaz:

```python
# En src/components/sidebar.py

# Usar key dinámica para el selectbox
selected_model = st.selectbox(
    "Selecciona un modelo",
    options=list(AVAILABLE_MODELS.keys()),
    format_func=lambda x: AVAILABLE_MODELS[x],
    index=list(AVAILABLE_MODELS.keys()).index(session_state.context["model"]) 
        if session_state.context["model"] in AVAILABLE_MODELS else 0,
    key=f"model_select_{session_state.context['model']}"  # Key dinámica
)

# Mostrar información sobre el modelo actual
if selected_model == session_state.context["model"]:
    st.success(f"Usando modelo: {AVAILABLE_MODELS[selected_model]}")
else:
    st.warning(f"Cambiando de {AVAILABLE_MODELS[session_state.context['model']]} a {AVAILABLE_MODELS[selected_model]}...")

# Si el modelo cambió, actualizar el contexto y forzar reinicio
if (selected_model != session_state.context["model"]):
    logger.info(f"Cambio de modelo: {session_state.context['model']} -> {selected_model}")
    session_state.context["model"] = selected_model
    config_changed = True
    
    # Forzar reinicio inmediato cuando cambia el modelo
    logger.info("Forzando reinicio de la aplicación para aplicar el cambio de modelo")
    st.rerun()
```

### Paso 5: Verificar el Modelo en Uso

Añadir verificación explícita del modelo antes de cada generación:

```python
# En src/components/chat.py

def handle_user_input(prompt, session_state, client, logger):
    # Verificar y registrar el modelo actual
    current_model = session_state.context["model"]
    model_obj = get_model(current_model)
    
    # Verificación explícita
    logger.info(f"Verificando modelo seleccionado: {current_model} ({get_model_display_name(current_model)})")
    
    # Mostrar información del modelo que se está utilizando
    with st.chat_message("system"):
        st.info(f"Generando respuesta con {get_model_display_name(current_model)}...")
    
    # Resto del código...
```

### Paso 6: Añadir Indicador Visual del Modelo Actual

```python
# En app.py

# Mostrar indicador del modelo actual
from src.models.config import get_model_display_name
st.markdown(f"**Modelo actual:** {get_model_display_name(session_state.context['model'])}")
```

## Buenas Prácticas

1. **Siempre usar key dinámica para widgets de selección de modelo**: Esto garantiza que Streamlit recree el widget cuando cambia el modelo.

2. **Forzar reinicio inmediato al cambiar de modelo**: Usar `st.rerun()` para asegurar que todos los componentes utilicen el nuevo modelo.

3. **Proporcionar feedback visual claro**: Mostrar qué modelo está activo en varios lugares de la interfaz.

4. **Registrar cambios de modelo**: Usar el sistema de logging para registrar cuándo y a qué modelo se cambia.

5. **Verificar el modelo antes de cada generación**: Comprobar explícitamente qué modelo se está utilizando antes de generar respuestas.

6. **Manejar límites de contexto específicos por modelo**: Ajustar el número de mensajes de contexto según las capacidades de cada modelo.

7. **Documentar las características de cada modelo**: Incluir información sobre las capacidades, limitaciones y casos de uso recomendados para cada modelo.

## Ejemplos de Integración

### Ejemplo 1: Integración de un Modelo de Groq

```python
# En src/models/groq_models.py

class MixtureLlama3(BaseGroqModel):
    """Modelo Mixtral-Llama-3 de Groq."""
    
    def __init__(self):
        super().__init__()
        self.id = "mixtral-llama-3-70b"
        self.display_name = "Mixtral-Llama-3 (70B)"
        self.max_context_messages = 12
```

### Ejemplo 2: Integración de un Modelo Agéntico

```python
# En src/models/agentic_models.py

class ClaudeAgentic(BaseAgenticModel):
    """Modelo Claude con capacidades agénticas."""
    
    def __init__(self):
        super().__init__()
        self.id = "anthropic/claude-3-opus"
        self.display_name = "Claude 3 Opus (Agéntico)"
        self.max_context_messages = 15
        self.is_agentic = True
        
    def get_available_tools(self):
        """Retorna las herramientas disponibles para este modelo."""
        return ["web_search", "code_execution", "file_analysis"]
```

### Ejemplo 3: Implementación de un Nuevo Cliente API

```python
# En src/api/anthropic_client.py

from src.api.base_client import BaseAPIClient
import anthropic

class AnthropicClient(BaseAPIClient):
    """Cliente para interactuar con la API de Anthropic."""
    
    def __init__(self, api_key=None, logger=None):
        self.api_key = api_key
        self.logger = logger
        self.client = None
        
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    # Implementación de los métodos requeridos...
```

---

Con esta guía, deberías poder integrar nuevos modelos en MetanoIA de manera correcta y robusta, evitando los problemas comunes relacionados con el cambio de modelo y garantizando una experiencia de usuario fluida y confiable.

Recuerda que la clave para una integración exitosa está en manejar correctamente el estado de Streamlit y proporcionar feedback visual claro al usuario sobre qué modelo está activo en cada momento.
