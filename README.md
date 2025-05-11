# MetanoIA

MetanoIA es un proyecto que va más allá de ser un simple chatbot. Es una plataforma modular y extensible desarrollada con Streamlit y la API de Groq (inicialmente), que permite interactuar con diferentes modelos de lenguaje y visión a través de una interfaz moderna y configurable. El proyecto busca ser un espacio de aprendizaje y experimentación con la IA, documentando el proceso de desarrollo y fomentando buenas prácticas de programación.

## Características

### Interfaz y Experiencia de Usuario
- Interfaz moderna con tema "Fresh Tech" con gradientes y efectos visuales
- Configuración en barra lateral para personalizar la experiencia
- Streaming de respuestas en tiempo real
- Persistencia de estado entre sesiones
- Carga y procesamiento de imágenes para modelos multimodales

### Soporte para Modelos de IA
- Integración con múltiples modelos de Groq:
  - DeepSeek-r1-distill-llama-70b
  - Meta-llama/llama-4-maverick-17b-128e-instruct (con capacidades de visión)
  - Meta-llama/llama-4-scout-17b-16e-instruct (con capacidades de visión)
  - Qwen-qwq-32b
- Arquitectura preparada para integrar otros proveedores de API

### Arquitectura Modular
- Diseño basado en clases abstractas para facilitar extensiones
- Separación clara de responsabilidades
- Sistema de registro (logging) detallado
- Caché de respuestas para optimizar rendimiento
- Manejo robusto de errores y excepciones
- Limitación dinámica del contexto según el modelo

### Capacidades de Visión
- Procesamiento y análisis de imágenes con modelos multimodales
- Redimensionamiento automático de imágenes para cumplir con límites técnicos
- Soporte para OCR (reconocimiento óptico de caracteres)
- Análisis de contenido visual en contexto de conversación
- Integración fluida entre contexto textual y visual

## Estructura del Proyecto

```
MetanoIA/
├── app.py                  # Archivo principal de la aplicación
├── chat_bot.py             # Versión anterior (monolítica) de la aplicación
├── docs/                   # Documentación del proyecto
│   ├── process.md          # Registro del proceso de desarrollo
│   ├── grimorio-proyecto.md # Información general del proyecto
│   └── problemas_y_propuestas.md # Registro de problemas y soluciones
├── src/                    # Código fuente modularizado
│   ├── api/                # Módulos para interactuar con APIs
│   │   ├── __init__.py
│   │   └── groq_client.py  # Cliente para la API de Groq
│   ├── components/         # Componentes de la interfaz de usuario
│   │   ├── __init__.py
│   │   ├── chat.py         # Componente de chat
│   │   └── sidebar.py      # Componente de barra lateral
│   ├── models/             # Configuración y gestión de modelos
│   │   ├── __init__.py
│   │   └── config.py       # Configuración de modelos disponibles
│   ├── utils/              # Utilidades generales
│   │   ├── __init__.py
│   │   ├── image_processor.py # Procesamiento de imágenes
│   │   ├── logger.py       # Configuración del sistema de logging
│   │   ├── session_state.py # Gestión del estado de la sesión
│   │   └── styles.py       # Estilos y temas de la aplicación
│   └── __init__.py
└── README.md               # Este archivo
```

## Requisitos

- Python 3.7+
- Streamlit
- Groq API
- PIL (Pillow) para procesamiento de imágenes
- Bibliotecas adicionales: logging, time, datetime, base64, uuid, io

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/Ellokoakarata/MetanoIA.git
cd MetanoIA
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tu clave API de Groq:
```bash
export GROQ_API_KEY="tu-clave-api"
```
O ingrésala directamente en la interfaz de la aplicación.

## Uso

1. Ejecuta la aplicación:
```bash
streamlit run app.py
```

2. Abre tu navegador en http://localhost:8501

3. Configura el modelo y parámetros en la barra lateral

4. ¡Comienza a chatear!

## Extensibilidad

El proyecto está diseñado para ser fácilmente extensible:

- Para agregar nuevos modelos: modifica `src/models/config.py` y crea clases en `src/models/`
- Para agregar nuevas APIs: crea un nuevo cliente en `src/api/` que herede de `BaseAPIClient`
- Para agregar nuevas herramientas: crea nuevos componentes en `src/components/`
- Para extender capacidades de visión: modifica `src/utils/image_processor.py` y actualiza el cliente API correspondiente

## Filosofía del Proyecto

MetanoIA representa más que una aplicación técnica; es un viaje de aprendizaje y experimentación con la IA donde:

- El proceso de desarrollo es tan valioso como el producto final
- Se documenta cada paso del camino para facilitar el aprendizaje
- Se promueve la comprensión profunda de los conceptos de programación
- Se busca crear una herramienta que contribuya al progreso y entendimiento de la IA

## Documentación

El proyecto mantiene una documentación detallada en la carpeta `docs/`:

- `process.md`: Registro cronológico del proceso de desarrollo
- `grimorio-proyecto.md`: Visión general y detalles técnicos del proyecto
- `problemas_y_propuestas.md`: Registro de desafíos y sus soluciones
- `integracion_apis.md`: Guía para integrar nuevos proveedores de API
- `integracion_vision.md`: Documentación sobre la implementación de capacidades de visión
- `manejo_contexto.md`: Explicación del sistema de manejo de contexto
- `integracion_modelos.md`: Guía para integrar nuevos modelos
