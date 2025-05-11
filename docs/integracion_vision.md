# Integración de Capacidades de Visión en MetanoIA

## Estado: Implementado (v1.0 - Mayo 2025)

Este documento describe la planificación y los pasos realizados para integrar capacidades de visión en MetanoIA, permitiendo que el sistema procese y analice imágenes junto con texto, manteniendo el contexto de la conversación.

## Índice

1. [Modelos Compatibles](#modelos-compatibles)
2. [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
3. [Arquitectura Propuesta](#arquitectura-propuesta)
4. [Gestión de Imágenes](#gestión-de-imágenes)
5. [Integración con el Contexto](#integración-con-el-contexto)
6. [Implementación Paso a Paso](#implementación-paso-a-paso)
7. [Ejemplos de Uso](#ejemplos-de-uso)

## Modelos Compatibles

Actualmente, se han integrado los siguientes modelos multimodales de Groq que soportan capacidades de visión:

- **meta-llama/llama-4-scout-17b-16e-instruct**: Modelo multimodal capaz de procesar texto e imágenes, con soporte para conversaciones multilingües y multi-turno.
- **meta-llama/llama-4-maverick-17b-128e-instruct**: Versión avanzada con mayor contexto.

Estos modelos permiten realizar tareas como:
- Responder preguntas sobre imágenes
- Generar descripciones de imágenes
- Reconocimiento óptico de caracteres (OCR)
- Análisis de contenido visual

## Limitaciones y Consideraciones

### Limitaciones Técnicas

1. **Tamaño máximo de solicitud**: 20MB para URLs de imágenes.
2. **Resolución máxima**: 33 megapíxeles (33,177,600 píxeles totales) por imagen.
3. **Tamaño máximo para imágenes codificadas en base64**: 4MB.
4. **Número recomendado de imágenes por solicitud**: Máximo 5 para obtener la mejor calidad y precisión.

### Consideraciones para MetanoIA

1. **Redimensionamiento de imágenes**: Será necesario implementar un sistema de redimensionamiento automático para garantizar que las imágenes no excedan los límites de resolución.
2. **Almacenamiento temporal**: Las imágenes subidas por el usuario deberán almacenarse temporalmente antes de ser procesadas.
3. **Gestión de memoria**: El procesamiento de imágenes puede aumentar significativamente el uso de memoria.
4. **Experiencia de usuario**: La interfaz debe proporcionar feedback claro sobre el procesamiento de imágenes.

## Arquitectura Propuesta

Para integrar capacidades de visión en MetanoIA, se propone la siguiente arquitectura:

### 1. Extensión de Clases Base

```python
# src/api/base_client.py
class BaseAPIClient(ABC):
    # Métodos existentes...
    
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

### 2. Implementación para Groq

```python
# src/api/groq_client.py
class GroqClient(BaseAPIClient):
    # Métodos existentes...
    
    def generate_response_with_image(self, model, messages, image_data, temperature, max_tokens, callback=None):
        """Implementación para Groq de la generación de respuestas con imágenes."""
        try:
            # Preparar el contenido del mensaje con imagen
            content = [
                {"type": "text", "text": messages[-1]["content"]}
            ]
            
            # Añadir la imagen según su tipo (URL o base64)
            if "url" in image_data:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_data["url"]}
                })
            elif "base64" in image_data:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data['base64']}"}
                })
            
            # Preparar los mensajes anteriores
            api_messages = messages[:-1]  # Todos los mensajes excepto el último
            
            # Añadir el mensaje con la imagen
            api_messages.append({
                "role": "user",
                "content": content
            })
            
            # Llamar a la API con streaming
            # Implementación similar a generate_streaming_response pero con el formato adecuado para imágenes
            # ...
            
        except Exception as e:
            # Manejo de errores
            # ...
```

### 3. Componente de Gestión de Imágenes

```python
# src/utils/image_processor.py
class ImageProcessor:
    """Clase para procesar y gestionar imágenes."""
    
    @staticmethod
    def resize_image(image_path, max_pixels=33177600):
        """
        Redimensiona una imagen si excede el número máximo de píxeles.
        
        Args:
            image_path (str): Ruta a la imagen.
            max_pixels (int): Número máximo de píxeles permitidos.
            
        Returns:
            str: Ruta a la imagen redimensionada.
        """
        # Implementación con PIL o similar
        # ...
    
    @staticmethod
    def encode_image(image_path):
        """
        Codifica una imagen en base64.
        
        Args:
            image_path (str): Ruta a la imagen.
            
        Returns:
            str: Imagen codificada en base64.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    @staticmethod
    def validate_image(image_path):
        """
        Valida que una imagen cumpla con los requisitos.
        
        Args:
            image_path (str): Ruta a la imagen.
            
        Returns:
            tuple: (bool, str) - Validez y mensaje de error si aplica.
        """
        # Implementación
        # ...
```

### 4. Extensión del Estado de Sesión

```python
# src/utils/session_state.py
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
            "enable_agentic": False,
            "enable_vision": False  # Nuevo campo para habilitar capacidades de visión
        }
    
    if "image_context" not in st.session_state:
        st.session_state.image_context = {
            "recent_images": [],  # Lista de imágenes recientes procesadas
            "image_descriptions": [],  # Descripciones generadas para las imágenes
            "max_stored_images": 5  # Número máximo de imágenes a almacenar en el contexto
        }
    
    return st.session_state
```

### 5. Componente de Interfaz para Imágenes en el Sidebar

La subida de imágenes se implementará en el sidebar, manteniendo la coherencia con la arquitectura actual donde todos los controles de configuración se encuentran en esta ubicación.

```python
# src/components/sidebar.py (dentro de render_sidebar)
# Después de las opciones de configuración de modelo y parámetros

# Sección de capacidades de visión
if model_obj and hasattr(model_obj, "supports_vision") and model_obj.supports_vision:
    st.subheader("Capacidades de Visión")
    
    # Activar/desactivar visión
    enable_vision = st.checkbox(
        "Activar procesamiento de imágenes",
        value=session_state.context.get("enable_vision", False),
        help="Permite que el modelo analice imágenes junto con texto."
    )
    
    # Si la visión está activada, mostrar opciones de carga de imágenes
    if enable_vision:
        uploaded_image = st.file_uploader(
            "Subir imagen para análisis",
            type=["jpg", "jpeg", "png"],
            help="La imagen se procesará junto con tu próximo mensaje."
        )
        
        if uploaded_image:
            # Mostrar la imagen
            st.image(uploaded_image, caption="Imagen cargada", use_column_width=True)
            
            # Opciones de procesamiento
            st.caption("Esta imagen se analizará con tu próximo mensaje.")
            
            # Guardar la imagen en el estado de sesión
            image_path = save_uploaded_image(uploaded_image)
            session_state.context["current_image"] = {
                "path": image_path,
                "base64": ImageProcessor.encode_image(image_path)
            }
            
            # Botón para eliminar la imagen
            if st.button("Eliminar imagen"):
                session_state.context.pop("current_image", None)
                st.rerun()
```

Esta implementación permite:
1. Mostrar las opciones de visión solo cuando se selecciona un modelo compatible
2. Activar/desactivar la funcionalidad de visión
3. Subir, previsualizar y eliminar imágenes desde el sidebar
4. Mantener la imagen en el estado de sesión para usarla con el próximo mensaje

## Gestión de Imágenes

### Redimensionamiento vs. Límites

Para manejar las limitaciones de tamaño y resolución, se propone:

1. **Enfoque híbrido**:
   - Establecer límites máximos para la carga de imágenes (por ejemplo, 10MB).
   - Implementar redimensionamiento automático para imágenes que excedan la resolución máxima (33 megapíxeles).
   - Mantener la relación de aspecto original para no distorsionar el contenido.

2. **Algoritmo de redimensionamiento**:
   - Calcular la relación entre píxeles actuales y máximos permitidos.
   - Aplicar esta relación para redimensionar proporcionalmente.
   - Utilizar interpolación de alta calidad para preservar detalles importantes.

3. **Feedback al usuario**:
   - Informar cuando una imagen ha sido redimensionada.
   - Mostrar las dimensiones originales y nuevas.
   - Ofrecer opciones para ajustar manualmente si es necesario.

## Integración con el Contexto

Es fundamental que la información extraída de las imágenes se integre inmediatamente en el contexto general de la conversación. Para lograrlo:

### 1. Almacenamiento en el Contexto

```python
# En src/components/chat.py
def handle_user_input_with_image(prompt, image_data, session_state, groq_client, logger):
    """
    Maneja la entrada del usuario con imagen y genera una respuesta.
    
    Args:
        prompt (str): Mensaje del usuario.
        image_data (dict): Datos de la imagen.
        session_state: Estado de la sesión de Streamlit.
        groq_client: Cliente de la API.
        logger: Logger para registrar información.
    """
    # Generar respuesta con imagen
    response = groq_client.generate_response_with_image(
        model=session_state.context["model"],
        messages=prepare_api_messages(session_state, session_state.context["model"], logger),
        image_data=image_data,
        temperature=session_state.context["temperature"],
        max_tokens=session_state.context["max_tokens"]
    )
    
    # Almacenar la imagen en el contexto
    if len(session_state.image_context["recent_images"]) >= session_state.image_context["max_stored_images"]:
        session_state.image_context["recent_images"].pop(0)
        session_state.image_context["image_descriptions"].pop(0)
    
    session_state.image_context["recent_images"].append(image_data)
    session_state.image_context["image_descriptions"].append(response["content"])
    
    # Agregar al historial de mensajes
    session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "has_image": True,
        "image_reference": len(session_state.image_context["recent_images"]) - 1
    })
    
    session_state.messages.append({
        "role": "assistant", 
        "content": response["content"], 
        "model_used": session_state.context["model"]
    })
```

### 2. Preparación de Mensajes con Contexto de Imágenes

```python
# En src/components/chat.py
def prepare_api_messages_with_vision(session_state, current_model, logger):
    """
    Prepara los mensajes para la API incluyendo contexto de imágenes.
    
    Args:
        session_state: Estado de la sesión de Streamlit.
        current_model: ID del modelo actual.
        logger: Logger para registrar información.
        
    Returns:
        list: Lista de mensajes preparados para la API.
    """
    # Código base similar a prepare_api_messages
    
    # Añadir resumen de imágenes al prompt del sistema si hay imágenes en el contexto
    if session_state.image_context["recent_images"]:
        image_context = "\n\n### Contexto de imágenes previas:\n"
        for i, desc in enumerate(session_state.image_context["image_descriptions"]):
            image_context += f"Imagen {i+1}: {desc[:200]}...\n"
        
        api_messages[0]["content"] += image_context
    
    # Resto del código
    # ...
```

## Implementación Paso a Paso

La implementación de capacidades de visión en MetanoIA se realizará en varias fases:

### Fase 1: Preparación de la Infraestructura

1. Extender las clases base para soportar imágenes.
2. Implementar el procesador de imágenes.
3. Modificar el estado de sesión para almacenar información de imágenes.

### Fase 2: Implementación de la Interfaz

1. Crear componente de carga de imágenes.
2. Integrar el componente en la interfaz principal.
3. Implementar feedback visual para el procesamiento de imágenes.

### Fase 3: Integración con la API

1. Implementar la función `generate_response_with_image` en el cliente de Groq.
2. Adaptar la preparación de mensajes para incluir imágenes.
3. Manejar las respuestas y actualizar el contexto.

### Fase 4: Pruebas y Optimización

1. Probar con diferentes tipos y tamaños de imágenes.
2. Optimizar el redimensionamiento y procesamiento.
3. Mejorar la integración del contexto visual con el textual.

## Ejemplos de Uso

Una vez implementada la funcionalidad de visión, los usuarios podrán:

### Análisis de Imágenes

Con la implementación en el sidebar, el flujo de trabajo sería:

1. El usuario activa el procesamiento de imágenes en el sidebar
2. Sube una imagen a través del componente de carga en el sidebar
3. Escribe un mensaje o pregunta en el chat principal
4. El sistema procesa automáticamente el mensaje junto con la imagen

```python
# En src/components/chat.py
def handle_user_input(prompt, session_state, groq_client, logger):
    """Maneja la entrada del usuario y genera una respuesta."""
    # Verificar si hay una imagen en el contexto actual
    if session_state.context.get("enable_vision", False) and "current_image" in session_state.context:
        # Procesar el mensaje con la imagen
        image_data = session_state.context["current_image"]
        handle_user_input_with_image(prompt, image_data, session_state, groq_client, logger)
        
        # Opcional: limpiar la imagen actual después de usarla
        # session_state.context.pop("current_image", None)
    else:
        # Procesar el mensaje normalmente (sin imagen)
        # Código existente...
```

### Conversación Multi-turno con Imágenes

Los usuarios podrán hacer preguntas de seguimiento sobre imágenes previamente cargadas, y el sistema mantendrá el contexto visual a lo largo de la conversación.

### OCR y Extracción de Texto

Para la extracción de texto (OCR), el usuario simplemente necesitaría:

1. Activar el procesamiento de imágenes en el sidebar
2. Subir la imagen que contiene texto
3. Escribir un mensaje como "Extrae todo el texto visible en esta imagen" en el chat principal

Podemos añadir atajos para mejorar la experiencia de usuario:

```python
# En src/components/sidebar.py (dentro de la sección de visión)
if uploaded_image:
    # Mostrar la imagen y opciones básicas...
    
    # Añadir atajos para tareas comunes
    st.subheader("Acciones rápidas")
    col1, col2 = st.columns(2)
    
    if col1.button("Describir imagen"):
        # Enviar automáticamente un mensaje al chat
        add_user_message("Describe detalladamente esta imagen", session_state)
        handle_user_input_with_image("Describe detalladamente esta imagen", 
                                    session_state.context["current_image"], 
                                    session_state, groq_client, logger)
    
    if col2.button("Extraer texto (OCR)"):
        add_user_message("Extrae todo el texto visible en esta imagen", session_state)
        handle_user_input_with_image("Extrae todo el texto visible en esta imagen", 
                                    session_state.context["current_image"], 
                                    session_state, groq_client, logger)
```

Esta implementación proporciona atajos convenientes para tareas comunes de procesamiento de imágenes directamente desde el sidebar, mejorando la experiencia de usuario mientras mantiene la flexibilidad para consultas personalizadas a través del chat principal.

## Implementación Actual

La integración de capacidades de visión se ha realizado siguiendo estas fases:

1. **Fase 1**: Integración básica con modelos de Groq ✅
   - Implementación de carga de imágenes desde la interfaz de usuario en la barra lateral
   - Soporte para análisis de imágenes y OCR
   - Integración con el contexto de conversación existente

2. **Fase 2**: Mejoras y optimizaciones ✅
   - Implementación de pre-procesamiento de imágenes (redimensionamiento, compresión)
   - Validación de límites de tamaño y resolución según restricciones de Groq
   - Gestión mejorada de errores y registro detallado

## Próximos Pasos

Para futuras versiones, se planean las siguientes mejoras:

1. **Fase 3**: Expansión a otros proveedores
   - Integrar con OpenAI y otros proveedores de API de visión
   - Implementar selección automática del mejor modelo según la tarea
   - Añadir capacidades avanzadas como segmentación y detección de objetos

2. **Fase 4**: Características avanzadas
   - Caché de imágenes para mejorar el rendimiento
   - Análisis de múltiples imágenes en una conversación
   - Generación de imágenes basada en descripciones textuales

## Conclusión

La integración de capacidades de visión en MetanoIA representa un paso importante en la evolución del proyecto, permitiendo una interacción más rica y contextual con los usuarios. Esta implementación mantiene el enfoque educativo del proyecto, no solo mejorando la funcionalidad, sino también sirviendo como ejemplo práctico de cómo integrar tecnologías multimodales en aplicaciones de IA conversacional.

La arquitectura modular implementada facilitará la futura integración de otros proveedores de API de visión como OpenAI, Claude, o Gemini, permitiendo a los usuarios experimentar con diferentes modelos y comparar sus capacidades.
