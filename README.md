# MetanoIA

Un chatbot modular avanzado desarrollado con Streamlit y la API de Groq, que permite interactuar con diferentes modelos de lenguaje a través de una interfaz moderna y configurable.

## Características

- Interfaz con tema "Fresh Tech" con gradientes y efectos visuales modernos
- Soporte para múltiples modelos de Groq:
  - DeepSeek-r1-distill-llama-70b
  - Meta-llama/llama-4-maverick-17b-128e-instruct
  - Meta-llama/llama-4-scout-17b-16e-instruct
  - Qwen-qwq-32b
- Configuración en barra lateral para seleccionar modelos y parámetros
- Sistema de registro (logging) que muestra información detallada en terminal
- Streaming de respuestas en tiempo real
- Persistencia de estado usando st.session_state
- Caché de respuestas usando @st.cache_data
- Manejo de errores y excepciones
- Limitación dinámica del contexto según el modelo

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
- Bibliotecas adicionales: logging, time, datetime

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

- Para agregar nuevos modelos: modifica `src/models/config.py`
- Para agregar nuevas APIs: crea un nuevo cliente en `src/api/`
- Para agregar nuevas herramientas: crea nuevos componentes en `src/components/`

## Documentación

Para más detalles sobre el desarrollo del proyecto, consulta los archivos en la carpeta `docs/`.
