# Integración de Speech-to-Text en MetanoIA

## Introducción

Este documento describe la integración de capacidades de reconocimiento de voz (Speech-to-Text) en el proyecto MetanoIA utilizando la API de Groq. Esta funcionalidad permite a los usuarios transcribir archivos de audio y utilizar el texto resultante como entrada para la conversación con el asistente.

La integración de Speech-to-Text complementa las capacidades multimodales del proyecto, añadiendo una nueva dimensión de interacción que permite a los usuarios comunicarse mediante voz, además de texto e imágenes.

## Modelos compatibles

Groq ofrece varios modelos de Whisper para la transcripción de audio, cada uno con diferentes características:

| Modelo | Descripción | Uso recomendado |
|--------|-------------|-----------------|
| `whisper-large-v3-turbo` | Versión optimizada para velocidad | Cuando la velocidad es prioritaria |
| `whisper-large-v3` | Modelo completo con mayor precisión | Para transcripciones multilingües precisas |
| `distil-whisper-large-v3-en` | Modelo destilado para inglés | Para contenido exclusivamente en inglés |

## Arquitectura de la integración

La integración de Speech-to-Text sigue la arquitectura modular de MetanoIA y se compone de:

1. **Componente de interfaz de usuario** (`src/components/audio.py`):
   - Proporciona widgets para subir archivos de audio
   - Permite seleccionar el modelo y el idioma
   - Gestiona la visualización y reproducción del audio

2. **Servicio de transcripción** (`src/api/audio_transcription.py`):
   - Implementa la comunicación con la API de Groq
   - Maneja la transcripción y traducción de audio
   - Procesa los resultados y errores

3. **Integración con el flujo de conversación** (modificaciones en `src/components/chat.py` y `app.py`):
   - Incorpora la transcripción como entrada de texto en la conversación
   - Mantiene el contexto entre diferentes interacciones
   - Gestiona la limpieza de archivos temporales

## Limitaciones técnicas

- **Tamaño máximo de archivo**: 25MB (tier gratuito) o 100MB (tier de desarrollo)
- **Formatos soportados**: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
- **Duración mínima facturada**: 10 segundos (incluso para archivos más cortos)
- **Idiomas**: Soporta múltiples idiomas, con mejor rendimiento en inglés

## Flujo de trabajo de la transcripción

1. El usuario sube un archivo de audio a través de la interfaz
2. Selecciona el modelo de transcripción y el idioma (opcional)
3. Inicia la transcripción haciendo clic en el botón correspondiente
4. El sistema procesa el audio y obtiene el texto transcrito
5. El texto se incorpora como un mensaje del usuario en la conversación
6. El asistente responde al contenido transcrito

## Implementación paso a paso

### 1. Componente de interfaz de usuario

El componente `audio.py` proporciona una interfaz para:
- Subir archivos de audio en diferentes formatos
- Reproducir el audio subido
- Seleccionar el modelo de transcripción y el idioma
- Iniciar el proceso de transcripción

### 2. Servicio de transcripción

El servicio `AudioTranscriber` en `audio_transcription.py`:
- Utiliza el cliente de Groq ya configurado
- Implementa métodos para transcribir y traducir audio
- Maneja errores y devuelve resultados estructurados

### 3. Integración con el chat

Las modificaciones en `chat.py` y `app.py`:
- Detectan cuando hay una transcripción pendiente
- Incorporan el texto transcrito como entrada del usuario
- Gestionan la limpieza de archivos temporales

## Uso educativo

Esta integración sirve como ejemplo práctico de:

1. **Procesamiento de lenguaje natural aplicado al habla**:
   - Cómo los modelos de IA convierten señales de audio en texto
   - Diferencias entre modelos de transcripción

2. **Integración de APIs externas**:
   - Comunicación con servicios de IA de terceros
   - Manejo de respuestas y errores

3. **Desarrollo de interfaces multimodales**:
   - Combinación de diferentes formas de entrada (texto, audio)
   - Gestión del estado y contexto entre interacciones

## Posibles mejoras futuras

1. **Grabación directa de audio**:
   - Implementar grabación en tiempo real cuando Streamlit lo soporte

2. **Procesamiento de archivos grandes**:
   - Añadir fragmentación automática para archivos que excedan los límites

3. **Análisis avanzado**:
   - Incorporar detección de hablantes
   - Añadir timestamps para navegar por la transcripción

4. **Traducción integrada**:
   - Implementar la traducción automática de audio a texto en otro idioma

## Conclusión

La integración de Speech-to-Text en MetanoIA amplía las capacidades de interacción del proyecto, manteniendo su filosofía educativa donde el usuario comprende cada parte del sistema. Esta funcionalidad no solo mejora la experiencia del usuario, sino que también sirve como ejemplo práctico de cómo las tecnologías de IA pueden trabajar juntas en un sistema integrado.
