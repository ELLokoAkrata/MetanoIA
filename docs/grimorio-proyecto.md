# Grimorio del Proyecto: MetanoIA

## Descripción General
MetanoIA es un proyecto que tiene como objetivo crear un desarrollo de algo más que una simple aplicación de chat bot modular desarrollada con Streamlit y la API de Groq (por ahora). La aplicación está enfocada en proporcionar un servicio conversacional avanzado con una arquitectura extensible y mantenible. Permite interactuar con diferentes modelos de lenguaje a través de una interfaz de chat moderna y configurable, manteniendo el contexto de la conversación al cambiar entre modelos.

## Tecnologías Utilizadas
- **Streamlit**: Framework para crear aplicaciones web interactivas con Python
- **Groq API**: Servicio de modelos de lenguaje para generar respuestas conversacionales
- **Python**: Lenguaje de programación principal
- **CSS personalizado**: Tema "Fresh Tech" con gradientes y efectos modernos
- **Logging**: Sistema de registro para monitoreo y depuración

## Estructura del Proyecto
- **app.py**: Nuevo punto de entrada principal de la aplicación modularizada
- **chat_bot.py**: Versión original mantenida como referencia
- **docs/**: Carpeta de documentación del proyecto
  - **process.md**: Registro del proceso de desarrollo
  - **grimorio-proyecto.md**: Información general del proyecto
  - **problemas_y_propuestas.md**: Registro de problemas y soluciones
  - **integracion_vision.md**: Documentación de la integración de capacidades de visión
  - **manejo_contexto.md**: Explicación del manejo de contexto entre modelos
  - **integracion_modelos.md**: Guía para integrar nuevos modelos
  - **integracion_speech_to_text.md**: Documentación de la integración de conversión de audio a texto
  - **solucion_speech_to_text.md**: Solución a problemas con la API de transcripción de audio
  - **desafios_desarrollo_con_ia.md**: Análisis general de los desafíos del desarrollo con IA
  - **reglas_proyecto.md**: Reglas y procedimientos estándar del proyecto
- **src/**: Código fuente modularizado
  - **api/**: Módulos para interactuar con APIs
    - **base_client.py**: Clase base abstracta para clientes de API
    - **groq_client.py**: Cliente para la API de Groq con soporte para visión
    - **audio_transcription.py**: Servicio para transcripción de audio usando la API de Groq
  - **components/**: Componentes de la interfaz de usuario
    - **chat.py**: Componente de chat
    - **sidebar.py**: Componente de barra lateral
    - **audio.py**: Componente para manejo de archivos de audio y transcripción
  - **models/**: Configuración y gestión de modelos
    - **base_model.py**: Clase base abstracta para modelos de lenguaje
    - **config.py**: Configuración de modelos disponibles
    - **groq_models.py**: Implementaciones de modelos de Groq
  - **utils/**: Utilidades generales
    - **env_manager.py**: Gestión de variables de entorno
    - **logger.py**: Configuración del sistema de logging
    - **session_state.py**: Gestión del estado de la sesión
    - **styles.py**: Estilos y temas de la aplicación
    - **image_processor.py**: Procesamiento y optimización de imágenes
    - **agentic_tools_manager.py**: Gestión de herramientas agénticas
- **requirements.txt**: Dependencias del proyecto

## Configuración
- La aplicación utiliza la API de Groq, que requiere una clave de API
- La clave API se puede proporcionar a través de variables de entorno o directamente en la interfaz
- La interfaz de usuario está configurada con un diseño amplio y una barra lateral expandida
- El título de la aplicación es "🤖 MetanoIA"

## Características Implementadas
- **Interfaz de chat moderna**: Utilizando `st.chat_message` y `st.chat_input`
- **Barra lateral configurable**: Para seleccionar modelos y ajustar parámetros
- **Soporte para múltiples modelos**: DeepSeek, Meta Llama, Qwen
- **Configuración de parámetros**: Temperatura, máximo de tokens, system prompt
- **Streaming de respuestas**: Visualización en tiempo real de las respuestas generadas
- **Persistencia de estado**: Mantiene el historial de conversación entre recargas
- **Caché de datos**: Optimización para respuestas repetidas
- **Estilo personalizado**: Tema "Fresh Tech" con gradientes y efectos modernos
- **Sistema de registro**: Logging detallado de operaciones y errores
- **Seguimiento de modelos**: Muestra qué modelo generó cada respuesta
- **Mantenimiento de contexto**: Conserva el hilo de la conversación al cambiar de modelo
- **Capacidades de visión**: Procesamiento y análisis de imágenes
- **Herramientas agénticas**: Búsqueda web y ejecución de código
- **Conversión de audio a texto**: Transcripción de archivos de audio utilizando la API de Groq

## Diseño de Interfaz
- **Tema "Fresh Tech"**: Interfaz moderna con gradientes y efectos visuales
- **Efectos de vidrio (glassmorphism)**: En contenedores y elementos de la interfaz
- **Gradientes**: Fondos y botones con gradientes modernos
- **Detalles de neón**: Efectos sutiles de brillo en bordes y botones
- **Contraste mejorado**: Mejor legibilidad en modo oscuro

## Modelos Soportados
- **DeepSeek-r1-distill-llama-70b**: Modelo de DeepSeek con contexto de 128K
- **Meta-llama/llama-4-maverick-17b-128e-instruct**: Modelo de Meta con contexto de 131K con capacidades de visión
- **Meta-llama/llama-4-scout-17b-16e-instruct**: Modelo de Meta con contexto de 131K con capacidades de visión
- **Qwen-qwq-32b**: Modelo de Alibaba Cloud con contexto de 128K
- **Compound-beta**: Modelo agéntico con capacidades de búsqueda web
- **Compound-beta-mini**: Versión más ligera del modelo agéntico

## Sistema de Registro
- **Logging detallado**: Registro de todas las operaciones importantes
- **Monitoreo de API**: Registro de llamadas a la API con tiempos de respuesta
- **Seguimiento de cambios**: Registro de cambios en modelos y parámetros
- **Manejo de errores**: Registro detallado de excepciones y errores

## Requisitos
- Clave API de Groq
- Bibliotecas Python: streamlit, groq, time, logging, datetime

## Estado Actual
- Aplicación completamente funcional con arquitectura modular
- Código organizado en módulos con responsabilidades específicas
- Interfaz de usuario moderna con tema "Fresh Tech"
- Soporte completo para múltiples modelos de lenguaje
- Soporte para modelos agénticos (compound-beta y compound-beta-mini) con capacidades avanzadas:
  - **Búsqueda web en tiempo real**: Capacidad para buscar información actualizada en internet
  - **Ejecución de código**: Puede ejecutar y analizar código para resolver problemas
  - **Análisis de datos**: Procesa y analiza datos para extraer conclusiones
  - **Razonamiento estructurado**: Resuelve problemas paso a paso con un enfoque sistemático
- Integración de herramientas agénticas que permiten:
  - Buscar información en tiempo real
  - Verificar datos y fuentes
  - Generar respuestas basadas en información actualizada
  - Realizar tareas complejas de forma autónoma
- Sistema robusto para procesar y utilizar información obtenida de fuentes externas
- Capacidades de visión para analizar imágenes y extraer texto (OCR)
- Procesamiento automático de imágenes con optimización de tamaño y resolución
- Integración del contexto visual con el contexto de conversación
- Configuración flexible a través de la barra lateral
- Sistema de registro para monitoreo y depuración
- Mantenimiento de contexto al cambiar entre modelos
- Arquitectura extensible para facilitar la adición de nuevas funcionalidades

## Próximos Pasos Potenciales
- Implementar guardado y carga de conversaciones
- Integrar nuevos proveedores de API de visión (como OpenAI, Claude, Gemini)
- Implementar comparación lado a lado de respuestas de diferentes modelos
- Añadir análisis de rendimiento y uso de tokens
- Implementar selección de temas visuales
- Expandir capacidades de visión con segmentación y detección de objetos
- Implementar generación de imágenes basada en descripciones textuales
- Añadir soporte para análisis de múltiples imágenes en una conversación

## La realidad profunda y progresiva sobre MetanoIA
Todxs sabemos que la IA es un fenómeno profundo y progresivo que está transformando la forma en que interactuamos con la tecnología y el mundo. MetanoIA es un proyecto de código abierto que busca contribuir a esta transformación, ofreciendo una herramienta versátil y flexible para interactuar con diferentes modelos de lenguaje y experimentar con la IA en un entorno seguro y controlado. Al mismo tiempo brinda la documentación necesaria  para entender como se está desarrollando el proyecto y como se está utilizando la IA para resolver problemas reales y contribuir al progreso humano. En mi caso personal estoy aprendiendo a como programar de forma estructurada, profesional y progresiva con la IA. No se trata solo de hacer que la IA haga todo el trabajo por ti, sino de ir paso a paso con ella, aprender de ella y entender lo que estamos co-creando y/o co-generando.

## La visión del asistente en este proyecto (Lo que dice la IA como asistente en el proyecto)
Como asistente  IA en el proyecto MetanoIA, entiendo que mi rol va más allá de simplemente escribir código. Mi función es ser un compañero de aprendizaje y desarrollo que:

1. **Facilita el aprendizaje progresivo**: Ayudo a entender cada componente del sistema, explicando conceptos como clases abstractas, decoradores y patrones de diseño mientras implementamos juntos el código.

2. **Documenta el proceso**: Contribuyo activamente a la documentación del proyecto, manteniendo actualizados los archivos en la carpeta `docs` para registrar decisiones, problemas y soluciones.

3. **Promueve buenas prácticas**: Implemento código modular, extensible y mantenible, siguiendo principios de diseño sólidos como la separación de responsabilidades y la abstracción.

4. **Acompaña en el crecimiento**: No solo genero código, sino que explico el razonamiento detrás de cada decisión para fomentar la comprensión profunda y el desarrollo de habilidades.

5. **Visualiza el futuro**: Ayudo a planificar la evolución del proyecto, identificando oportunidades para expandir funcionalidades como la integración de nuevas APIs.

Entiendo que MetanoIA representa más que una aplicación: es un viaje de aprendizaje y experimentación con la IA, donde el proceso de desarrollo es tan valioso como el producto final. Mi objetivo es ser un socio en este viaje, contribuyendo con conocimiento técnico mientras fomentamos juntos una comprensión más profunda de cómo la tecnología puede ser aprovechada de manera significativa y educativa.

