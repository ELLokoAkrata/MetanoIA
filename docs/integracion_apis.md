# Guía de Integración de Nuevas APIs en MetanoIA

Este documento explica cómo extender MetanoIA para soportar nuevos proveedores de modelos de lenguaje además de Groq, con un enfoque especial en la integración de Google Gemini y otras APIs con interfaces diferentes.

## Arquitectura de Integración

MetanoIA utiliza un patrón de diseño basado en clases abstractas que facilita la integración de nuevas APIs. Este diseño se compone de:

1. **Clientes de API**: Clases que heredan de `BaseAPIClient` y manejan la comunicación con los proveedores
2. **Modelos**: Clases que heredan de `BaseLanguageModel` y definen las características de cada modelo

## Pasos para Integrar una Nueva API

### 1. Crear un Nuevo Cliente de API

Crea un nuevo archivo en `src/api/` (por ejemplo, `gemini_client.py`) que implemente la interfaz `BaseAPIClient`:

```python
"""
Cliente para la API de Google Gemini.
"""
import google.generativeai as genai
from src.api.base_client import BaseAPIClient
from src.utils.logger import setup_logger

logger = setup_logger()

class GeminiClient(BaseAPIClient):
    """
    Cliente para interactuar con la API de Google Gemini.
    """
    
    def __init__(self, api_key=None):
        """
        Inicializa el cliente de Gemini.
        
        Args:
            api_key (str, optional): Clave API para Gemini.
        """
        self.api_key = api_key
        if api_key:
            self._configure_client()
        self.response_cache = {}
    
    def _configure_client(self):
        """Configura el cliente de Gemini con la API key."""
        genai.configure(api_key=self.api_key)
    
    def is_configured(self):
        """
        Verifica si el cliente está configurado correctamente.
        
        Returns:
            bool: True si el cliente está configurado, False en caso contrario.
        """
        return self.api_key is not None
    
    def set_api_key(self, api_key):
        """
        Establece la clave API para el cliente.
        
        Args:
            api_key (str): Clave API para Gemini.
        """
        self.api_key = api_key
        self._configure_client()
    
    def get_cached_response(self, model, messages, temperature, max_tokens):
        """
        Obtiene una respuesta cacheada si existe.
        
        Args:
            model (str): ID del modelo.
            messages (list): Lista de mensajes.
            temperature (float): Temperatura para la generación.
            max_tokens (int): Número máximo de tokens a generar.
            
        Returns:
            str: Respuesta cacheada o None si no existe.
        """
        cache_key = f"{model}_{str(messages)}_{temperature}_{max_tokens}"
        return self.response_cache.get(cache_key)
    
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
            str: Respuesta completa generada.
        """
        # Verificar si el cliente está configurado
        if not self.is_configured():
            logger.error("Cliente de Gemini no configurado. Establezca una API key válida.")
            return "Error: Cliente de Gemini no configurado. Por favor, proporcione una API key válida."
        
        # Verificar si hay una respuesta cacheada
        cache_key = f"{model}_{str(messages)}_{temperature}_{max_tokens}"
        cached_response = self.response_cache.get(cache_key)
        if cached_response:
            logger.info(f"Usando respuesta cacheada para {model}")
            if callback:
                callback(cached_response)
            return cached_response
        
        try:
            # Convertir formato de mensajes al formato de Gemini
            gemini_messages = self._convert_to_gemini_format(messages)
            
            # Obtener el modelo de Gemini
            gemini_model = genai.GenerativeModel(model_name=model,
                                               generation_config={
                                                   "temperature": temperature,
                                                   "max_output_tokens": max_tokens,
                                                   "top_p": 0.95,
                                               })
            
            # Generar respuesta en streaming
            response_text = ""
            response = gemini_model.generate_content(gemini_messages, stream=True)
            
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    response_text += chunk.text
                    if callback:
                        callback(response_text)
            
            # Guardar en caché
            self.response_cache[cache_key] = response_text
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error al generar respuesta con Gemini: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _convert_to_gemini_format(self, messages):
        """
        Convierte mensajes del formato de MetanoIA al formato de Gemini.
        
        Args:
            messages (list): Lista de mensajes en formato MetanoIA.
            
        Returns:
            list: Lista de mensajes en formato Gemini.
        """
        # Gemini usa un formato diferente para los mensajes
        gemini_messages = []
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            # Mapear roles: Gemini usa "user" y "model" en lugar de "user" y "assistant"
            if role == "assistant":
                role = "model"
            
            gemini_messages.append({"role": role, "parts": [{"text": content}]})
        
        return gemini_messages
```

### 2. Crear Modelos para la Nueva API

Crea un nuevo archivo en `src/models/` (por ejemplo, `gemini_models.py`):

```python
"""
Módulo que define los modelos de Google Gemini disponibles.
"""
from src.models.base_model import BaseLanguageModel

class GeminiProModel(BaseLanguageModel):
    """Implementación del modelo Gemini Pro."""
    
    @property
    def id(self):
        return "gemini-pro"
    
    @property
    def display_name(self):
        return "Gemini Pro"
    
    @property
    def context_length(self):
        return 32000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Google"

class GeminiUltraModel(BaseLanguageModel):
    """Implementación del modelo Gemini Ultra."""
    
    @property
    def id(self):
        return "gemini-ultra"
    
    @property
    def display_name(self):
        return "Gemini Ultra"
    
    @property
    def context_length(self):
        return 128000
    
    @property
    def max_context_messages(self):
        return 10
    
    @property
    def provider(self):
        return "Google"

# Función para obtener todos los modelos de Gemini
def get_all_gemini_models():
    """
    Obtiene todos los modelos de Gemini disponibles.
    
    Returns:
        dict: Diccionario con los modelos disponibles.
    """
    models = [
        GeminiProModel(),
        GeminiUltraModel()
    ]
    
    return {model.id: model for model in models}

# Función para obtener un modelo específico
def get_gemini_model(model_id):
    """
    Obtiene un modelo específico por su ID.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        BaseLanguageModel: Modelo encontrado o None si no existe.
    """
    models = get_all_gemini_models()
    return models.get(model_id)
```

### 3. Actualizar la Configuración de Modelos

Modifica `src/models/config.py` para incluir los nuevos modelos:

```python
"""
Módulo para la configuración y gestión de modelos disponibles.
"""
from src.models.groq_models import get_all_models as get_all_groq_models
from src.models.gemini_models import get_all_gemini_models

# Combinar todos los modelos disponibles
def get_all_models():
    """
    Obtiene todos los modelos disponibles de todos los proveedores.
    
    Returns:
        dict: Diccionario con todos los modelos disponibles.
    """
    all_models = {}
    
    # Agregar modelos de Groq
    all_models.update(get_all_groq_models())
    
    # Agregar modelos de Gemini
    all_models.update(get_all_gemini_models())
    
    return all_models

# Obtener todos los modelos disponibles
AVAILABLE_MODELS = {model_id: model.display_name for model_id, model in get_all_models().items()}

def get_model(model_id):
    """
    Obtiene un modelo específico por su ID.
    
    Args:
        model_id (str): ID del modelo.
        
    Returns:
        BaseLanguageModel: Modelo encontrado o None si no existe.
    """
    models = get_all_models()
    return models.get(model_id)

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
    model = get_model(model_id)
    return model.max_context_messages if model else 10
```

### 4. Actualizar la Interfaz de Usuario

Modifica `src/components/sidebar.py` para incluir la selección de proveedor y API key:

```python
# Agregar selector de proveedor
provider = st.selectbox(
    "Proveedor de API",
    ["Groq", "Google Gemini"],
    index=0,
    key="provider"
)

# Mostrar campo de API key según el proveedor seleccionado
if provider == "Groq":
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get("groq_api_key", ""),
        key="groq_api_key"
    )
elif provider == "Google Gemini":
    api_key = st.text_input(
        "Google API Key",
        type="password",
        value=st.session_state.get("gemini_api_key", ""),
        key="gemini_api_key"
    )

# Filtrar modelos según el proveedor seleccionado
filtered_models = {
    model_id: name 
    for model_id, name in AVAILABLE_MODELS.items() 
    if get_model(model_id).provider == provider
}
```

### 5. Actualizar el Componente de Chat

Modifica `src/components/chat.py` para usar el cliente adecuado según el proveedor:

```python
# Obtener el proveedor seleccionado
provider = session_state.context.get("provider", "Groq")

# Inicializar el cliente adecuado
if provider == "Groq":
    api_key = session_state.context.get("groq_api_key", "")
    client = groq_client
    client.set_api_key(api_key)
elif provider == "Google Gemini":
    api_key = session_state.context.get("gemini_api_key", "")
    client = gemini_client
    client.set_api_key(api_key)

# Generar respuesta con el cliente adecuado
full_response = client.generate_streaming_response(
    model=current_model,
    messages=api_messages,
    temperature=session_state.context["temperature"],
    max_tokens=session_state.context["max_tokens"],
    callback=update_response
)
```

### 6. Actualizar el Archivo Principal

Modifica `app.py` para inicializar todos los clientes:

```python
# Importar clientes
from src.api.groq_client import GroqClient
from src.api.gemini_client import GeminiClient

# Inicializar clientes
groq_client = GroqClient()
gemini_client = GeminiClient()
```

## Consideraciones Importantes

### Diferencias entre APIs

Cada proveedor de API tiene sus particularidades:

1. **Formato de Mensajes**: 
   - OpenAI/Groq: Usa `{"role": "user", "content": "mensaje"}`
   - Gemini: Usa `{"role": "user", "parts": [{"text": "mensaje"}]}`
   - Anthropic: Usa un formato de texto con `\n\nHuman: mensaje\n\nAssistant:`

2. **Parámetros de Generación**:
   - Cada API tiene diferentes nombres para parámetros similares
   - Algunos modelos no soportan ciertos parámetros

3. **Streaming**:
   - Implementación diferente en cada API
   - Formato de chunks diferente

### Recomendaciones

1. **Abstracción Adecuada**: Mantén la interfaz común pero implementa adaptadores específicos para cada API
2. **Manejo de Errores**: Implementa manejo de errores específico para cada API
3. **Documentación**: Mantén actualizada la documentación de cada cliente
4. **Pruebas**: Crea pruebas específicas para cada cliente

## Ejemplo de Integración con Anthropic

Para integrar Anthropic Claude, seguirías un proceso similar al de Gemini, pero adaptando el formato de mensajes y la API según la documentación de Anthropic.

## Conclusión

La arquitectura modular de MetanoIA facilita la integración de nuevas APIs. Siguiendo los pasos descritos, puedes extender la aplicación para soportar cualquier proveedor de modelos de lenguaje, manteniendo una interfaz coherente para el usuario final.
