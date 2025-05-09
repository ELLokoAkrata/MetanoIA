# Problemas y Propuestas

## Problemas Identificados

### 2025-05-09: Error de importación en chat_bot.py
**Problema**: Se detectó un error en el archivo `chat_bot.py` donde se intentaba utilizar el módulo `os` sin haberlo importado previamente, lo que generaba el siguiente error:
```
NameError: name 'os' is not defined
```

**Impacto**: La aplicación no podía ejecutarse correctamente ya que no podía acceder a la clave API de Groq almacenada en las variables de entorno.

### 2025-05-09: Funcionalidad básica limitada
**Problema**: La aplicación solo tenía una configuración básica sin funcionalidad de chat implementada y sin soporte para múltiples modelos.

**Impacto**: No era posible interactuar con el chatbot ni configurar diferentes parámetros para la generación de respuestas.

### 2025-05-09: Problemas de legibilidad en la interfaz
**Problema**: La interfaz tenía problemas de contraste, con contenedores blancos que dificultaban la lectura del texto.

**Impacto**: La experiencia de usuario se veía afectada por la dificultad para leer el contenido de la aplicación.

### 2025-05-09: Cambio de modelo no efectivo
**Problema**: Al cambiar de modelo en la barra lateral, no se aplicaba correctamente el cambio y se seguía utilizando el modelo predeterminado.

**Impacto**: No era posible probar y comparar diferentes modelos de lenguaje, limitando la funcionalidad principal de la aplicación.

### 2025-05-09: Error al enviar campos personalizados a la API
**Problema**: Se estaban enviando campos personalizados (`model_used`) en los mensajes a la API de Groq, lo que generaba un error:
```
Error code: 400 - {'error': {'message': "'messages.2' : for 'role:assistant' the following must be satisfied[('messages.2' : property 'model_used' is unsupported, did you mean 'role'?)]"}
```

**Impacto**: La aplicación fallaba al intentar generar respuestas después de cambiar de modelo.

### 2025-05-09: Límite de tokens excedido en modelos de Llama
**Problema**: Al acumular muchos mensajes en una conversación, se excede el límite de tokens por minuto (TPM) de la API de Groq, especialmente con los modelos Llama:
```
groq.APIStatusError: Error code: 413 - {'error': {'message': 'Request too large for model `meta-llama/llama-4-maverick-17b-128e-instruct` in organization `org_01hvyf1saverv8m45x6879pnc4` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requested 6029, please reduce your message size and try again. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
```

**Impacto**: La aplicación no podía generar respuestas cuando la conversación se volvía demasiado larga, limitando la utilidad del chatbot en conversaciones extensas.

## Propuestas de Solución

### 2025-05-09: Agregar importación faltante
**Propuesta**: Agregar la importación del módulo `os` al principio del archivo.

**Implementación**: Se modificó el archivo `chat_bot.py` para incluir la importación:
```python
import os
import streamlit as st
from groq import Groq
```

**Estado**: ✅ Implementado

### 2025-05-09: Implementar interfaz de chat completa
**Propuesta**: Desarrollar una interfaz de chat completa con soporte para múltiples modelos, configuración de parámetros y streaming de respuestas.

**Implementación**: Se reescribió completamente el archivo `chat_bot.py` para incluir funcionalidades avanzadas de chat.

**Estado**: ✅ Implementado

### 2025-05-09: Implementar tema "Fresh Tech"
**Propuesta**: Mejorar la interfaz con un diseño moderno y tecnológico que resuelva los problemas de legibilidad.

**Implementación**: Se creó un tema personalizado con gradientes, efectos de vidrio y mejor contraste:
```css
/* Tema base con gradiente para toda la aplicación */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    color: #e2e8f0 !important;
}

/* Estilos para mensajes de chat con efecto de vidrio */
.stChatMessage {
    background-color: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    /* Más estilos... */
}
```

**Estado**: ✅ Implementado

### 2025-05-09: Implementar sistema de registro y corregir cambio de modelo
**Propuesta**: Añadir un sistema de logging detallado y corregir el problema con el cambio de modelos.

**Implementación**: 
1. Se agregó un sistema de logging completo:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("psycho-bot")
```

2. Se modificó la selección de modelo para forzar una recarga cuando cambia:
```python
if (selected_model != st.session_state.context["model"]):
    logger.info(f"Cambio de modelo: {st.session_state.context['model']} -> {selected_model}")
    st.session_state.context["model"] = selected_model
    # Forzar recarga para aplicar el cambio inmediatamente
    st.rerun()
```

3. Se implementó un seguimiento del modelo usado para cada respuesta:
```python
st.session_state.messages.append({"role": "assistant", "content": full_response, "model_used": current_model})
```

**Estado**: ✅ Implementado

### 2025-05-09: Corregir error de campos personalizados en la API
**Propuesta**: Filtrar los campos personalizados antes de enviar los mensajes a la API de Groq.

**Implementación**: Se modificó la preparación de mensajes para la API:
```python
# Preparar mensajes para la API (filtrando campos personalizados)
api_messages = [
    {"role": "system", "content": st.session_state.context["system_prompt"]}
]

# Añadir mensajes del historial filtrando campos personalizados
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        # Solo incluir campos estándar (role y content)
        api_messages.append({"role": msg["role"], "content": msg["content"]})
```

**Estado**: ✅ Implementado

### 2025-05-09: Implementar limitación dinámica del contexto
**Propuesta**: Limitar dinámicamente el número de mensajes enviados a la API según el modelo utilizado para evitar exceder los límites de tokens por minuto (TPM).

**Implementación**: Se modificó el código para limitar el contexto de forma dinámica según el modelo:
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

**Estado**: ✅ Implementado

## Propuestas Futuras

### Manejo seguro de claves API
**Propuesta**: Implementar un método más seguro para manejar las claves API, como utilizar un archivo `.env` con la biblioteca `python-dotenv`.

**Beneficios**:
- Mayor seguridad para las credenciales
- Facilidad para configurar el entorno de desarrollo
- Prevención de exposición accidental de claves en el código fuente

**Estado**: 📝 Pendiente de implementación

### Guardado de conversaciones
**Propuesta**: Implementar funcionalidad para guardar y cargar conversaciones anteriores.

**Beneficios**:
- Permitiría a los usuarios continuar conversaciones anteriores
- Facilitaría el análisis de conversaciones para mejorar el sistema
- Mejoraría la experiencia de usuario al mantener un historial accesible

**Estado**: 📝 Pendiente de implementación

### Procesamiento de archivos
**Propuesta**: Añadir soporte para cargar y procesar archivos (PDF, texto, etc.) como contexto para las conversaciones.

**Beneficios**:
- Permitiría al chatbot responder preguntas basadas en documentos específicos
- Ampliaría las capacidades del sistema para casos de uso más avanzados
- Facilitaría la creación de asistentes especializados en dominios específicos

**Estado**: 📝 Pendiente de implementación

### Comparación de modelos lado a lado
**Propuesta**: Implementar una funcionalidad para comparar respuestas de diferentes modelos a la misma pregunta.

**Beneficios**:
- Facilitaría la evaluación de la calidad de diferentes modelos
- Permitiría identificar las fortalezas y debilidades de cada modelo
- Mejoraría la experiencia educativa al mostrar diferentes enfoques

**Estado**: 📝 Pendiente de implementación

### Análisis de rendimiento y uso de tokens
**Propuesta**: Añadir métricas de rendimiento y conteo de tokens para cada modelo.

**Beneficios**:
- Permitiría optimizar el uso de recursos
- Facilitaría la comparación de eficiencia entre modelos
- Ayudaría a estimar costos de uso de la API

**Estado**: 📝 Pendiente de implementación
