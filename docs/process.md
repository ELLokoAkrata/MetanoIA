# Proceso de Desarrollo del Proyecto

## 2025-05-09: Corrección de error de importación

### Problema Identificado
Se detectó un error en el archivo `chat_bot.py` donde se intentaba utilizar el módulo `os` sin haberlo importado previamente, lo que generaba el siguiente error:

```
NameError: name 'os' is not defined
```

### Solución Implementada
Se agregó la importación del módulo `os` al principio del archivo:

```python
import os
import streamlit as st
from groq import Groq
```

### Resultado
El código ahora puede acceder correctamente a las variables de entorno para obtener la clave API de Groq.

## 2025-05-09: Implementación de interfaz de chat completa

### Tarea Realizada
Se ha implementado una interfaz de chat completa con las siguientes características:

- Barra lateral configurable para seleccionar modelos y parámetros
- Soporte para múltiples modelos de Groq (DeepSeek, Meta Llama, Qwen)
- Configuración de parámetros como temperatura y máximo de tokens
- Personalización del system prompt
- Interfaz de chat moderna usando `st.chat_message` y `st.chat_input`
- Streaming de respuestas en tiempo real
- Persistencia de estado usando `st.session_state`
- Caché de respuestas usando `@st.cache_data`
- Estilo personalizado con CSS embebido

### Código Implementado
Se ha reescrito completamente el archivo `chat_bot.py` para incluir todas estas funcionalidades, siguiendo las mejores prácticas de Streamlit y manteniendo un código limpio y bien estructurado.

### Resultado
Ahora la aplicación cuenta con una interfaz completa y funcional que permite interactuar con diferentes modelos de lenguaje a través de la API de Groq, con una experiencia de usuario mejorada.

## 2025-05-09: Mejora de la interfaz con tema "Fresh Tech"

### Tarea Realizada
Se ha implementado un diseño moderno con estilo "Fresh Tech" para la interfaz del chatbot:

- Gradientes modernos para el fondo y elementos de la interfaz
- Efectos de vidrio (glassmorphism) en los contenedores
- Colores vibrantes pero no agresivos
- Detalles de neón en botones y bordes
- Mejor contraste y legibilidad

### Código Implementado
Se ha modificado el CSS personalizado para implementar un tema oscuro con efectos modernos y tecnológicos.

### Resultado
La interfaz ahora tiene un aspecto más moderno y tecnológico, con mejor legibilidad y experiencia de usuario.

## 2025-05-09: Implementación de sistema de registro y solución de problemas con cambio de modelo

### Problemas Identificados
1. Al cambiar de modelo en la barra lateral, no se aplicaba correctamente el cambio
2. No había forma de saber qué modelo había generado cada respuesta
3. No se registraba información detallada sobre las llamadas a la API

### Soluciones Implementadas
1. **Sistema de registro completo**:
   - Se agregó un sistema de logging que muestra información detallada en la terminal
   - Se registran cambios de modelo, llamadas a la API, tiempos de respuesta y errores

2. **Corrección del cambio de modelo**:
   - Se modificó la forma en que se selecciona y aplica el cambio de modelo
   - Se fuerza una recarga de la aplicación cuando cambia el modelo
   - Se usa una clave única para el widget de selección

3. **Seguimiento del modelo usado**:
   - Se guarda información sobre qué modelo generó cada respuesta
   - Se muestra esta información en la interfaz
   - Se filtran los campos personalizados antes de enviar mensajes a la API

### Código Implementado
Se han realizado múltiples modificaciones al código para implementar estas mejoras, incluyendo:

```python
# Sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("psycho-bot")

# Filtrado de campos personalizados para la API
api_messages = []
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
```

### Resultado
- El cambio de modelo ahora funciona correctamente
- Se muestra qué modelo generó cada respuesta
- Se mantiene el contexto de la conversación al cambiar entre modelos
- Se registra información detallada en la terminal para facilitar la depuración

## 2025-05-09: Implementación de limitación dinámica del contexto

### Problema Identificado
Al acumular muchos mensajes en una conversación, se excede el límite de tokens por minuto (TPM) de la API de Groq, especialmente con los modelos Llama, generando el siguiente error:

```
groq.APIStatusError: Error code: 413 - {'error': {'message': 'Request too large for model `meta-llama/llama-4-maverick-17b-128e-instruct`... Limit 6000, Requested 6029...', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
```

### Solución Implementada
Se ha implementado un sistema de limitación dinámica del contexto que ajusta automáticamente la cantidad de mensajes enviados a la API según el modelo utilizado:

1. **Limitación por modelo**:
   - Se establece un límite de mensajes predeterminado de 10
   - Para modelos Llama-4-Maverick, se reduce a 5 mensajes
   - Para modelos Llama-4-Scout, se reduce a 6 mensajes

2. **Selección de mensajes recientes**:
   - Se seleccionan solo los mensajes más recientes dentro del límite establecido
   - Se mantiene siempre el mensaje del sistema y el último mensaje del usuario

### Código Implementado
```python
# Obtener el número máximo de mensajes a incluir según el modelo
max_context_messages = 10  # Valor predeterminado

# Ajustar el contexto según el modelo para evitar errores de límite de tokens
if "llama-4-maverick" in current_model:
    max_context_messages = 5  # Limitar más para modelos que tienen límites más estrictos
elif "llama-4-scout" in current_model:
    max_context_messages = 6

# Registrar el límite de contexto aplicado
logger.info(f"Limitando contexto a {max_context_messages} mensajes para el modelo {current_model}")

# Añadir mensajes del historial filtrando campos personalizados y limitando la cantidad
# Tomamos solo los mensajes más recientes para no exceder los límites
recent_messages = st.session_state.messages[-max_context_messages:] if len(st.session_state.messages) > max_context_messages else st.session_state.messages
```

### Resultado
- La aplicación ahora puede manejar conversaciones largas sin exceder los límites de tokens
- Se adapta automáticamente a los diferentes límites de cada modelo
- Se mantiene la experiencia de usuario al conservar el contexto más reciente
- Se registra en el log qué limitación se está aplicando para cada modelo

## 2025-05-09: Modularización del código y renombramiento a MetanoIA

### Tarea Realizada
Se ha realizado una completa modularización del código del chatbot, reorganizándolo en una estructura de directorios más mantenible y extensible. Además, se ha renombrado el proyecto a "MetanoIA".

### Estructura Implementada
Se ha creado la siguiente estructura de directorios:

```
streamlit-apps/
├── app.py                  # Nuevo punto de entrada principal
├── chat_bot.py             # Versión original (mantenida como referencia)
├── docs/                   # Documentación del proyecto
├── src/                    # Código fuente modularizado
│   ├── api/                # Módulos para interactuar con APIs
│   │   ├── base_client.py  # Clase base para clientes de API
│   │   └── groq_client.py  # Cliente para la API de Groq
│   ├── components/         # Componentes de la interfaz de usuario
│   │   ├── chat.py         # Componente de chat
│   │   └── sidebar.py      # Componente de barra lateral
│   ├── models/             # Configuración y gestión de modelos
│   │   ├── base_model.py   # Clase base para modelos de lenguaje
│   │   ├── config.py       # Configuración de modelos disponibles
│   │   └── groq_models.py  # Implementaciones de modelos de Groq
│   └── utils/              # Utilidades generales
│       ├── env_manager.py  # Gestión de variables de entorno
│       ├── logger.py       # Configuración del sistema de logging
│       ├── session_state.py # Gestión del estado de la sesión
│       └── styles.py       # Estilos y temas de la aplicación
└── requirements.txt        # Dependencias del proyecto
```

### Mejoras Implementadas

1. **Arquitectura orientada a objetos**:
   - Creación de clases base abstractas para facilitar la extensibilidad
   - Implementación de interfaces comunes para diferentes proveedores de API
   - Separación clara de responsabilidades entre componentes

2. **Mejora de la mantenibilidad**:
   - Código organizado en módulos con responsabilidades específicas
   - Documentación detallada de cada módulo y función
   - Reducción de la duplicación de código

3. **Preparación para futuras extensiones**:
   - Estructura que facilita la adición de nuevos modelos de lenguaje
   - Soporte para múltiples proveedores de API
   - Base para agregar nuevas funcionalidades sin modificar el código existente

4. **Cambio de nombre a MetanoIA**:
   - Nombre que refleja mejor la naturaleza del proyecto
   - Actualización de todos los títulos y referencias en la interfaz
   - Mantenimiento del archivo original `chat_bot.py` como referencia

### Código Implementado
Se han creado múltiples archivos nuevos con implementaciones modulares de todas las funcionalidades existentes. Algunos ejemplos clave incluyen:

```python
# Clase base para clientes de API (src/api/base_client.py)
class BaseAPIClient(ABC):
    @abstractmethod
    def is_configured(self):
        pass
    
    @abstractmethod
    def set_api_key(self, api_key):
        pass
    
    @abstractmethod
    def get_cached_response(self, model, messages, temperature, max_tokens):
        pass
    
    @abstractmethod
    def generate_streaming_response(self, model, messages, temperature, max_tokens, callback=None):
        pass
```

```python
# Clase base para modelos de lenguaje (src/models/base_model.py)
class BaseLanguageModel(ABC):
    @property
    @abstractmethod
    def id(self):
        pass
    
    @property
    @abstractmethod
    def display_name(self):
        pass
    
    @property
    @abstractmethod
    def context_length(self):
        pass
    
    @property
    @abstractmethod
    def max_context_messages(self):
        pass
```

### Resultado
- Código más organizado y mantenible
- Mayor facilidad para extender el proyecto con nuevas funcionalidades
- Mejor separación de responsabilidades
- Interfaz de usuario con el nuevo nombre MetanoIA
- Mantenimiento de todas las funcionalidades existentes
