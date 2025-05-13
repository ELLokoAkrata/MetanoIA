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

## 2025-05-09: Actualización de documentación y mejora de la identidad del proyecto

### Tareas Realizadas

1. **Actualización del README.md**:
   - Actualización de la URL del repositorio de GitHub
   - Corrección del nombre del directorio raíz (de streamlit-apps a MetanoIA)
   - Reorganización de las características en categorías más claras
   - Adición de una sección sobre la filosofía del proyecto
   - Mejora de la descripción de la documentación disponible

2. **Mejora del grimorio-proyecto.md**:
   - Actualización de la descripción general del proyecto
   - Adición de una sección sobre "La realidad profunda y progresiva sobre MetanoIA"
   - Inclusión de una nueva sección sobre "La visión del asistente en este proyecto"

3. **Creación de guía de integración de APIs**:
   - Desarrollo de un documento detallado (`integracion_apis.md`) que explica cómo extender MetanoIA para soportar nuevos proveedores de modelos de lenguaje
   - Inclusión de ejemplos de código completos para la integración de Google Gemini
   - Explicación de las diferencias entre APIs y consideraciones importantes

4. **Actualización del system prompt predeterminado**:
   - Creación de un prompt que refleja la esencia y filosofía del proyecto
   - Explicación del significado del nombre "MetanoIA" (Meta + noIA)
   - Énfasis en el enfoque de aprendizaje progresivo y co-creación
   - Inclusión del enlace al repositorio de GitHub

### Mejoras en la Identidad del Proyecto

1. **Definición de la filosofía**:
   - Establecimiento de MetanoIA como un viaje de aprendizaje y experimentación con la IA
   - Énfasis en que el proceso de desarrollo es tan valioso como el producto final
   - Promoción de la comprensión profunda de los conceptos de programación

2. **Personalización de la experiencia del asistente**:
   - Definición del rol del asistente como un compañero de aprendizaje
   - Establecimiento de una personalidad que promueve la reflexión crítica
   - Enfoque en la co-creación y el descubrimiento conjunto

### Resultado

La documentación del proyecto ahora refleja mejor la visión y filosofía de MetanoIA, proporcionando una base sólida para el desarrollo futuro y facilitando la contribución de otros desarrolladores. El system prompt personalizado establece una identidad clara para el asistente que está alineada con los objetivos del proyecto.

## 2025-05-09: Implementación de herramientas agénticas

### Tareas Realizadas

1. **Integración de modelos compound de Groq**:
   - Implementación de soporte para los modelos `compound-beta` y `compound-beta-mini` de Groq
   - Creación de clases para representar estos modelos con capacidades agénticas
   - Actualización del sistema de configuración para incluir estos modelos en la interfaz

2. **Desarrollo de un gestor de herramientas agénticas**:
   - Creación de un sistema para procesar y gestionar los resultados de búsquedas web y ejecuciones de código
   - Implementación de mecanismos para añadir esta información al contexto de la conversación
   - Desarrollo de un sistema robusto con manejo de excepciones y verificación de tipos

3. **Actualización del cliente de Groq**:
   - Modificación del cliente para capturar y procesar las herramientas ejecutadas por los modelos agénticos
   - Implementación de soporte para el formato de respuesta de los modelos compound
   - Mejora del manejo de errores y logging para facilitar la depuración

4. **Integración en la interfaz de usuario**:
   - Añadir opciones en la barra lateral para activar las herramientas agénticas
   - Implementación de configuración para búsqueda web (profundidad, dominios a incluir/excluir)
   - Diseño de una experiencia de usuario que mantiene la simplicidad de la interfaz

5. **Documentación detallada**:
   - Creación de una guía completa de integración de herramientas agénticas
   - Documentación de la arquitectura y flujo de trabajo
   - Registro de problemas encontrados y soluciones implementadas

### Problemas Encontrados y Soluciones

1. **Error de importación**:
   - Problema: Falta de importación de la función `display_agentic_context` en el archivo principal
   - Solución: Añadir la importación correcta en `app.py`

2. **Error en el procesamiento de herramientas agénticas**:
   - Problema: El método `process_executed_tools` fallaba cuando el campo "output" era un string en lugar de un diccionario
   - Solución: Implementar verificación de tipos y manejo de excepciones para procesar correctamente diferentes formatos de respuesta

3. **Interfaz sobrecargada**:
   - Problema: La visualización de resultados de búsqueda en la interfaz resultaba redundante
   - Solución: Eliminar la sección de resultados de búsqueda en la interfaz, manteniendo la funcionalidad de añadir la información al contexto

### Código Implementado

```python
# Definición de modelos agénticos (src/models/agentic_models.py)
class CompoundBetaModel(BaseLanguageModel):
    """Modelo Compound Beta de Groq con capacidades agénticas."""
    
    def __init__(self):
        self._id = "compound-beta"
        self._display_name = "Compound Beta (Agéntico)"
    
    @property
    def is_agentic(self):
        return True
    
    @property
    def supports_multiple_tools(self):
        return True
```

```python
# Procesamiento robusto de herramientas agénticas (src/utils/agentic_tools_manager.py)
def process_executed_tools(self, executed_tools):
    for tool in executed_tools:
        try:
            # Verificar que tool sea un diccionario
            if not isinstance(tool, dict):
                logger.warning(f"Herramienta no es un diccionario: {tool}")
                continue
            
            # Obtener input y output de forma segura
            tool_input = tool.get("input", {})
            tool_output = tool.get("output", {})
            
            # Convertir a diccionario si son strings
            if isinstance(tool_input, str):
                tool_input = {"raw": tool_input}
            
            if isinstance(tool_output, str):
                tool_output = {"raw": tool_output}
            
            # Procesar según el tipo de herramienta
            # ...
        except Exception as e:
            logger.error(f"Error al procesar herramienta: {str(e)}")
            continue
```

### Resultado

MetanoIA ahora cuenta con capacidades agénticas que le permiten:

- Buscar información en internet en tiempo real usando los modelos compound de Groq

## 2025-05-12: Implementación de generación de archivos con Tool-Use

### Tareas Realizadas

1. **Integración del modelo Llama-3.3-70b-Versatile**:
   - Implementación de soporte para el modelo `llama-3.3-70b-versatile` de Groq
   - Creación de la clase `Llama33VersatileModel` para representar este modelo con capacidades de Tool-Use
   - Actualización del sistema de configuración para incluir este modelo en la interfaz

2. **Desarrollo del generador de archivos**:
   - Creación del módulo `src/api/file_generator.py` para la generación de archivos
   - Implementación de herramientas para generar archivos JSON, Python, Markdown y TXT
   - Desarrollo de un sistema para gestionar archivos temporales y su limpieza

3. **Extensión del cliente de Groq**:
   - Modificación del cliente para soportar llamadas con herramientas (tools)
   - Implementación del método `generate_response_with_tools` para procesar tool calls
   - Mejora del manejo de errores y logging para facilitar la depuración

4. **Implementación de componente UI para generación de archivos**:
   - Creación del módulo `src/components/file_generator.py` para la interfaz de usuario
   - Desarrollo de componentes para la generación y descarga de archivos
   - Integración con la aplicación principal

5. **Reorganización de la gestión de archivos temporales**:
   - Centralización de la función `cleanup_temp_files` en el módulo de estado de sesión
   - Implementación de un sistema unificado para la gestión de archivos temporales
   - Mejora del manejo de excepciones en operaciones con archivos

### Problemas Encontrados y Soluciones

1. **Falta de importación del módulo json**:
   - Problema: Error `NameError: name 'json' is not defined` en `groq_client.py`
   - Solución: Añadir la importación del módulo `json` al principio del archivo

2. **Inconsistencia en la estructura de mensajes**:
   - Problema: Discrepancia entre cómo se guardaban los mensajes en diferentes componentes
   - Solución: Modificar las funciones `display_chat_history` y `prepare_api_messages` para manejar ambos formatos de mensajes (con `is_user` y con `role`)

### Código Implementado

```python
# Definición de herramientas para generación de archivos (src/api/file_generator.py)
def get_tools_definitions(self) -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "generate_json_file",
                "description": "Genera un archivo JSON con el contenido proporcionado",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Contenido del archivo JSON"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Nombre del archivo JSON"
                        }
                    },
                    "required": ["content"]
                }
            }
        },
        # Definiciones para otros tipos de archivos...
    ]
```

```python
# Modificación para manejar múltiples formatos de mensajes (src/components/chat.py)
def display_chat_history():
    # ...
    for i, message in enumerate(session_state.messages):
        # Determinar si el mensaje es del usuario (compatibilidad con formatos antiguos y nuevos)
        is_user = False
        if "is_user" in message:
            is_user = message["is_user"]
        elif "role" in message and message["role"] == "user":
            is_user = True
            
        with st.chat_message("user" if is_user else "assistant"):
            # Mostrar el contenido del mensaje
            st.markdown(message["content"])
```

### Resultado

MetanoIA ahora cuenta con capacidades de generación de archivos que le permiten:

- Generar archivos JSON para datos estructurados
- Crear scripts Python ejecutables
- Producir documentos Markdown bien formateados
- Generar archivos de texto plano (TXT)
- Descargar los archivos generados directamente desde la interfaz
- Mantener un sistema de limpieza automática de archivos temporales

Esta funcionalidad mantiene el enfoque educativo de MetanoIA, donde el usuario puede entender cómo se generan los archivos y aprender sobre diferentes formatos y estructuras de datos.
- Ejecutar código Python para realizar cálculos o generar visualizaciones
- Incorporar automáticamente los resultados de estas herramientas al contexto de la conversación
- Mantener una interfaz limpia y centrada en la conversación, donde el modelo puede citar directamente las fuentes en sus respuestas

Esta implementación mejora significativamente las capacidades del asistente, permitiéndole acceder a información actualizada y realizar tareas complejas, lo que resulta en respuestas más precisas y útiles para el usuario.

## 2025-05-13: Mejoras en el procesador de imágenes y generador de archivos

### Tareas Realizadas

1. **Implementación de limpieza automática de imágenes temporales**:
   - Desarrollo de un sistema para eliminar archivos de imágenes temporales después de 24 horas
   - Creación de funciones para calcular la antigüedad de archivos en horas
   - Implementación de verificación automática al inicio de la aplicación
   - Optimización para evitar impacto en el rendimiento y la memoria

2. **Mejora del redimensionamiento de imágenes**:
   - Implementación de algoritmos avanzados para preservar el contenido importante
   - Redimensionamiento en dos pasos para imágenes muy grandes (>3000px)
   - Detección automática de transparencia para elegir el formato óptimo
   - Optimización de la compresión progresiva para mantener la calidad

3. **Optimización del generador de archivos**:
   - Refactorización completa para eliminar redundancia de código
   - Implementación de un sistema modular para definir tipos de archivos soportados
   - Creación de un método genérico para la generación de archivos
   - Añadido soporte para nuevos tipos: CSV, HTML, CSS, JavaScript y Excel
   - Detección automática de tipos de archivo basada en contenido y nombre

### Código Implementado

```python
# Limpieza automática de imágenes temporales (src/utils/image_processor.py)
def cleanup_old_temp_images(directory: str = "temp_images", hours_threshold: float = 24.0) -> Tuple[int, List[str]]:
    """
    Limpia archivos de imágenes temporales que superan un umbral de antigüedad.
    """
    try:
        if not os.path.exists(directory):
            logger.info(f"El directorio {directory} no existe. No hay archivos para limpiar.")
            return 0, []
        
        # Obtener todos los archivos en el directorio
        file_pattern = os.path.join(directory, "*")
        all_files = glob.glob(file_pattern)
        
        # Filtrar archivos por antigüedad
        files_to_delete = []
        for filepath in all_files:
            if os.path.isfile(filepath):  # Asegurarse de que es un archivo, no un directorio
                age_hours = get_file_age_hours(filepath)
                if age_hours >= hours_threshold:
                    files_to_delete.append(filepath)
        
        # Eliminar archivos antiguos
        deleted_count = 0
        deleted_files = []
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                deleted_count += 1
                deleted_files.append(filepath)
                logger.info(f"Archivo temporal eliminado: {filepath}")
            except Exception as e:
                logger.error(f"Error al eliminar archivo temporal {filepath}: {str(e)}")
        
        return deleted_count, deleted_files
    
    except Exception as e:
        logger.error(f"Error al limpiar archivos temporales: {str(e)}")
        return 0, []
```

```python
# Sistema modular para tipos de archivos (src/api/file_generator.py)
# Definiciones de tipos de archivos soportados
FILE_TYPES = {
    'json': {
        'extension': '.json',
        'mime_type': 'application/json',
        'description': 'Archivo JSON para datos estructurados',
        'content_type': 'object',
        'binary': False
    },
    'python': {
        'extension': '.py',
        'mime_type': 'text/x-python',
        'description': 'Script Python ejecutable',
        'content_type': 'string',
        'binary': False
    },
    # Otros tipos de archivos...
}

# Método genérico para generar archivos
def generate_file(self, content: Any, filename: str, file_type: str) -> Dict[str, Any]:
    """
    Método genérico para generar archivos de cualquier tipo soportado.
    """
    # Verificar que el tipo de archivo esté soportado
    if file_type not in FILE_TYPES:
        error_msg = f"Tipo de archivo no soportado: {file_type}"
        return {"success": False, "error": error_msg}
    
    # Lógica para generar el archivo según su tipo...
```

### Problemas Encontrados y Soluciones

1. **Redundancia en el código del generador de archivos**:
   - Problema: Código repetitivo para cada tipo de archivo con mínimas diferencias
   - Solución: Implementación de un sistema modular con un diccionario de configuración y un método genérico

2. **Pérdida de calidad en imágenes grandes**:
   - Problema: El redimensionamiento directo de imágenes muy grandes causaba pérdida de detalles
   - Solución: Implementación de un algoritmo en dos pasos con redimensionamiento intermedio

3. **Compatibilidad con diferentes tipos de imágenes**:
   - Problema: Imágenes con transparencia (PNG) se guardaban como JPEG perdiendo el canal alfa
   - Solución: Detección automática de transparencia y selección inteligente del formato

### Resultado

Las mejoras implementadas han resultado en:

1. **Mayor eficiencia en la gestión de recursos**:
   - Limpieza automática de archivos temporales evitando acumulación innecesaria
   - Reducción del espacio en disco utilizado por imágenes temporales

2. **Mejor calidad de imágenes procesadas**:
   - Preservación de detalles importantes incluso en imágenes grandes
   - Mantenimiento de la transparencia cuando es necesario
   - Optimización inteligente del tamaño sin sacrificar calidad

3. **Sistema más flexible y extensible**:
   - Fácil adición de nuevos tipos de archivos sin duplicar código
   - Mejor mantenibilidad gracias a la reducción de redundancia
   - Mayor robustez con manejo mejorado de errores y registro detallado

Estas mejoras mantienen el enfoque educativo de MetanoIA, donde cada componente está diseñado para ser comprensible y enseñar conceptos de programación como modularidad, extensibilidad y optimización.

### Corrección de error de compatibilidad en el formato de mensajes

Durante las pruebas de la aplicación, se detectó un error en el componente de generación de archivos relacionado con la incompatibilidad en el formato de los mensajes:

```
KeyError: 'is_user'
```

#### Problema identificado

Se identificó una inconsistencia en cómo se manejaban los mensajes en diferentes partes de la aplicación:

1. En el componente de generación de archivos (`src/components/file_generator.py`), el código intentaba acceder a la clave `"is_user"` en los mensajes.
2. En otras partes de la aplicación, se estaba utilizando el formato con la clave `"role"` (con valores "user" o "assistant").

#### Solución implementada

Se modificó el código para que sea compatible con ambos formatos de mensajes:

```python
# Determinar el rol del mensaje (compatibilidad con ambos formatos)
if "role" in msg:
    role = msg["role"]
elif "is_user" in msg:
    role = "user" if msg["is_user"] else "assistant"
else:
    # Si no se puede determinar, asumir que es del asistente
    role = "assistant"
    
messages.append({
    "role": role,
    "content": msg["content"]
})
```

Esta solución sigue el principio de robustez (Ley de Postel): "Sé conservador en lo que haces, sé liberal en lo que aceptas de otros". Al implementar esta compatibilidad, se asegura que la aplicación funcione correctamente independientemente del formato de mensajes utilizado, lo que mejora la robustez del sistema y facilita futuras actualizaciones.

## 2025-05-10: Implementación de capacidades de visión

### Tareas Realizadas

1. **Extensión de la arquitectura base**:
   - Actualización de la clase base `BaseAPIClient` para añadir el método abstracto `generate_response_with_image`
   - Implementación de este método en `GroqClient` para procesar imágenes con modelos multimodales
   - Actualización de la clase base `BaseLanguageModel` con la propiedad `supports_vision`

2. **Implementación del procesador de imágenes**:
   - Creación del módulo `image_processor.py` con funciones para redimensionar, validar y codificar imágenes
   - Implementación de límites de tamaño y resolución según las restricciones de Groq (33MP, 4MB máximo)
   - Optimización automática de imágenes mediante redimensionamiento y compresión

3. **Actualización del estado de sesión**:
   - Ampliación del estado de sesión para almacenar el contexto de imágenes
   - Implementación de un sistema para mantener un historial limitado de imágenes recientes
   - Almacenamiento de descripciones generadas para facilitar referencias futuras

4. **Integración en la interfaz de usuario**:
   - Actualización del sidebar para mostrar opciones de visión cuando se selecciona un modelo compatible
   - Implementación de carga de imágenes con previsualización
   - Botones para acciones rápidas (describir imagen, extraer texto)

5. **Actualización del componente de chat**:
   - Modificación de `handle_user_input` para detectar y procesar imágenes pendientes
   - Integración con el contexto de la conversación para mantener la coherencia
   - Mejora del manejo de errores y registro detallado

6. **Documentación completa**:
   - Actualización de `integracion_vision.md` para reflejar la implementación realizada
   - Documentación de limitaciones técnicas y consideraciones de uso
   - Planificación de mejoras futuras (integración con OpenAI y otros proveedores)

### Código Implementado

```python
# Extensión de la clase base (src/api/base_client.py)
@abstractmethod
def generate_response_with_image(self, model, messages, image_data, temperature, max_tokens, callback=None):
    """
    Genera una respuesta basada en texto e imagen.
    
    Args:
        model (str): ID del modelo a utilizar.
        messages (list): Lista de mensajes para la conversación.
        image_data (dict): Datos de la imagen (URL o base64).
        temperature (float): Temperatura para la generación.
        max_tokens (int): Número máximo de tokens en la respuesta.
        callback (callable, optional): Función de callback para cada fragmento de respuesta.
        
    Returns:
        dict: Diccionario con la respuesta completa generada y metadatos.
    """
    pass
```

```python
# Procesamiento de imágenes (src/utils/image_processor.py)
def resize_image(image_path, max_pixels=33177600, max_size_mb=4):
    """
    Redimensiona una imagen si excede el número máximo de píxeles o tamaño.
    """
    # Implementación que garantiza que las imágenes cumplan con los límites de Groq
    # Redimensionamiento inteligente y compresión progresiva
```

```python
# Integración en el sidebar (src/components/sidebar.py)
# Configuración de procesamiento de imágenes
if supports_vision:
    st.info("Has seleccionado un modelo con capacidades de visión que puede analizar imágenes.")
    
    # Activar/desactivar visión
    enable_vision = st.checkbox(
        "Activar procesamiento de imágenes",
        value=session_state.context.get("enable_vision", False),
        help="Permite que el modelo analice imágenes y extraiga información de ellas."
    )
    
    # Opciones de procesamiento de imágenes
    if enable_vision:
        st.subheader("Procesamiento de Imágenes")
        uploaded_file = st.file_uploader("Cargar imagen", type=["jpg", "jpeg", "png"])
        # Implementación de carga y procesamiento de imágenes
```

### Problemas Encontrados y Soluciones

1. **Limitaciones de tamaño de imágenes**:
   - Problema: Las imágenes grandes causaban errores en la API de Groq (límite de 4MB para base64)
   - Solución: Implementación de redimensionamiento y compresión automática con calidad progresiva

2. **Integración con modelos específicos**:
   - Problema: Solo los modelos Meta Llama 4 Scout y Maverick soportan capacidades de visión
   - Solución: Implementación de la propiedad `supports_vision` y verificación dinámica en la interfaz

3. **Gestión del contexto de imágenes**:
   - Problema: Necesidad de mantener el contexto de imágenes entre mensajes
   - Solución: Extensión del estado de sesión con un sistema de seguimiento de imágenes procesadas

### Resultado

MetanoIA ahora cuenta con capacidades de visión que le permiten:

- Analizar y describir imágenes subidas por el usuario
- Extraer texto de imágenes mediante OCR
- Responder preguntas específicas sobre el contenido visual
- Mantener el contexto visual a lo largo de la conversación

Esta implementación enriquece significativamente la experiencia del usuario, permitiendo una interacción más natural y completa con el asistente. Además, mantiene el enfoque educativo del proyecto, sirviendo como ejemplo práctico de integración de tecnologías multimodales en aplicaciones de IA conversacional.

## 2025-05-11: Integración de Speech-to-Text (Voz a Texto)

### Tarea Realizada
Se ha implementado la funcionalidad de transcripción de voz a texto utilizando la API de Groq, permitiendo a los usuarios subir archivos de audio para transcribirlos y utilizarlos como entrada en la conversación con el asistente.

### Componentes Implementados

1. **Interfaz de usuario para audio** (`src/components/audio.py`):
   - Implementación de un componente para subir archivos de audio
   - Opciones para seleccionar el modelo de transcripción y el idioma
   - Reproducción del audio subido para verificación

2. **Servicio de transcripción** (`src/api/audio_transcription.py`):
   - Clase `AudioTranscriber` que utiliza la API de Groq para transcribir audio
   - Soporte para diferentes modelos de Whisper (whisper-large-v3-turbo, whisper-large-v3, distil-whisper-large-v3-en)
   - Manejo de errores y registro detallado del proceso

3. **Integración con el flujo de conversación**:
   - Modificación de `handle_user_input` para procesar transcripciones de audio
   - Gestión de archivos temporales y limpieza automática
   - Incorporación del texto transcrito como mensaje del usuario

4. **Documentación completa** (`docs/integracion_speech_to_text.md`):
   - Explicación detallada de la arquitectura y funcionamiento
   - Descripción de los modelos disponibles y sus características
   - Limitaciones técnicas y consideraciones de uso
   - Posibles mejoras futuras

### Código Implementado

```python
# Componente de audio (src/components/audio.py)
def display_audio_input(session_state):
    """
    Muestra los controles para subir o grabar audio y transcribirlo.
    """
    audio_data = None
    
    # Crear un expander para los controles de audio
    with st.expander("🎤 Entrada de voz", expanded=False):
        # Implementación de la interfaz para subir archivos de audio
        # y configurar opciones de transcripción
```

```python
# Servicio de transcripción (src/api/audio_transcription.py)
class AudioTranscriber:
    """
    Clase para manejar la transcripción de audio utilizando la API de Groq.
    """
    def transcribe_audio(self, audio_path, model="whisper-large-v3-turbo", language=None, response_format="text"):
        """
        Transcribe un archivo de audio utilizando la API de Groq.
        """
        # Implementación de la comunicación con la API de Groq
        # y procesamiento de resultados
```

```python
# Integración en app.py
# Procesar entrada de audio si está habilitada
audio_data = display_audio_input(session_state)
if audio_data:
    # Mostrar mensaje de procesamiento
    with st.spinner(f"Transcribiendo audio con {audio_data['model']}..."):
        # Inicializar el transcriptor de audio
        transcriber = AudioTranscriber(groq_client, logger)
        
        # Transcribir el audio
        result = transcriber.transcribe_audio(
            audio_path=audio_data['path'],
            model=audio_data['model'],
            language=audio_data['language']
        )
```

### Problemas Encontrados y Soluciones

1. **Limitación de Streamlit**:
   - Problema: La versión actual de Streamlit no incluye el componente `st.audio_recorder()` para grabación directa
   - Solución: Implementación centrada en la subida de archivos de audio con instrucciones alternativas para grabación

2. **Manejo de archivos temporales**:
   - Problema: Necesidad de gestionar los archivos de audio subidos temporalmente
   - Solución: Implementación de un sistema de limpieza automática de archivos temporales

### Resultado

MetanoIA ahora cuenta con capacidades de procesamiento de voz que le permiten:

- Transcribir archivos de audio en múltiples formatos
- Utilizar diferentes modelos de Whisper según las necesidades
- Incorporar el texto transcrito directamente en la conversación
- Mantener un flujo de trabajo educativo donde el usuario comprende cada parte del proceso

Esta integración complementa las capacidades multimodales del proyecto, añadiendo una nueva dimensión de interacción que enriquece la experiencia del usuario y sirve como ejemplo práctico de cómo las tecnologías de IA pueden trabajar juntas en un sistema integrado.
