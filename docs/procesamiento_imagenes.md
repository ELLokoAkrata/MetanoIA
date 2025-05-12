# Procesamiento de Imágenes en MetanoIA

## Introducción

Este documento explica cómo MetanoIA procesa imágenes para integrarlas con modelos de lenguaje multimodales, con especial énfasis en la codificación base64 y su importancia en el flujo de trabajo.

## Índice

1. [¿Qué es base64 y por qué lo usamos?](#qué-es-base64-y-por-qué-lo-usamos)
2. [Flujo completo de procesamiento de imágenes](#flujo-completo-de-procesamiento-de-imágenes)
3. [Limitaciones técnicas y soluciones](#limitaciones-técnicas-y-soluciones)
4. [Ejemplos prácticos](#ejemplos-prácticos)
5. [Consideraciones de rendimiento](#consideraciones-de-rendimiento)

## ¿Qué es base64 y por qué lo usamos?

### Definición básica

Base64 es un sistema de codificación que convierte datos binarios en una cadena de texto ASCII. Utiliza 64 caracteres diferentes (A-Z, a-z, 0-9, + y /) para representar cualquier secuencia de bytes.

### ¿Por qué necesitamos base64 para imágenes?

1. **Limitaciones de JSON y APIs REST**:
   - Las APIs REST como Groq utilizan JSON para transmitir datos
   - JSON no puede contener datos binarios directamente
   - Las imágenes son datos binarios por naturaleza

2. **Alternativas consideradas**:
   - **URLs de imágenes**: Requieren que la imagen esté accesible públicamente
   - **Archivos multipart**: No compatibles con todas las APIs de modelos de lenguaje
   - **Base64**: Solución universal compatible con todas las APIs

### Ventajas específicas en MetanoIA

1. **Compatibilidad universal**:
   - Funciona con cualquier API de modelo de lenguaje (Groq, OpenAI, etc.)
   - No requiere servidores externos para almacenar imágenes

2. **Procesamiento en memoria**:
   - Permite manipular imágenes sin necesidad de guardarlas permanentemente
   - Facilita la implementación de transformaciones como redimensionamiento

3. **Integración con el contexto de conversación**:
   - Las imágenes codificadas pueden almacenarse como parte del historial
   - Permite referencias futuras a imágenes previamente procesadas

## Flujo completo de procesamiento de imágenes

### 1. Carga de la imagen

```
Usuario → Sube imagen → Streamlit → Datos binarios en memoria
```

Cuando un usuario sube una imagen a través de la interfaz de Streamlit, obtenemos los datos binarios de la imagen en memoria.

### 2. Preprocesamiento

```
Datos binarios → Validación → Redimensionamiento → Optimización
```

Antes de enviar la imagen al modelo:
- Verificamos el formato (JPEG, PNG, etc.)
- Comprobamos y ajustamos el tamaño (píxeles)
- Optimizamos la calidad para cumplir con límites de tamaño

### 3. Codificación base64

```
Datos binarios optimizados → Codificación base64 → Cadena de texto ASCII
```

Convertimos los datos binarios de la imagen a una cadena de texto base64:
```python
# Ejemplo simplificado
import base64
imagen_base64 = base64.b64encode(datos_binarios).decode('utf-8')
```

### 4. Integración en la solicitud API

```
Cadena base64 → Formato JSON → API de Groq
```

La cadena base64 se integra en el formato específico requerido por la API:
```json
{
  "messages": [
    {"role": "user", "content": [
      {"type": "text", "text": "Describe esta imagen"},
      {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQ..."}}
    ]}
  ]
}
```

### 5. Procesamiento en el servidor

```
API de Groq → Decodificación base64 → Imagen reconstruida → Modelo multimodal → Respuesta
```

En el servidor:
- La API decodifica la cadena base64 a datos binarios
- Reconstruye la imagen original
- El modelo multimodal procesa la imagen junto con el texto
- Genera una respuesta basada en ambos

## Limitaciones técnicas y soluciones

### 1. Tamaño máximo de solicitud

**Problema**: Groq limita el tamaño de las solicitudes a 20MB para URLs y 4MB para imágenes base64.

**Solución implementada**:
- Redimensionamiento automático de imágenes
- Compresión progresiva para mantener calidad aceptable
- Verificación previa de tamaño para evitar errores

```python
def resize_image(image_path, max_pixels=33177600, max_size_mb=4):
    """
    Redimensiona una imagen si excede el número máximo de píxeles o tamaño.
    Implementa compresión progresiva hasta cumplir con el límite de tamaño.
    """
    # Implementación en src/utils/image_processor.py
```

### 2. Sobrecarga de datos

**Problema**: La codificación base64 aumenta el tamaño aproximadamente un 33% respecto a los datos binarios originales.

**Solución implementada**:
- Optimización previa de imágenes
- Almacenamiento eficiente en el contexto de conversación
- Limpieza periódica de imágenes no utilizadas

### 3. Compatibilidad de modelos

**Problema**: No todos los modelos soportan procesamiento de imágenes.

**Solución implementada**:
- Detección automática de modelos compatibles
- Interfaz adaptativa que solo muestra opciones de imagen cuando es posible
- Mensajes claros al usuario sobre las capacidades disponibles

## Ejemplos prácticos

### Ejemplo 1: Descripción de imagen

```python
# Flujo simplificado para describir una imagen
imagen_subida = st.file_uploader("Cargar imagen", type=["jpg", "jpeg", "png"])
if imagen_subida:
    # 1. Leer datos binarios
    datos_binarios = imagen_subida.getvalue()
    
    # 2. Optimizar imagen
    datos_optimizados = ImageProcessor.resize_image(datos_binarios)
    
    # 3. Codificar en base64
    imagen_base64 = base64.b64encode(datos_optimizados).decode('utf-8')
    
    # 4. Crear mensaje para la API
    mensaje = [
        {"type": "text", "text": "Describe esta imagen en detalle."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}}
    ]
    
    # 5. Enviar a la API y mostrar respuesta
    respuesta = groq_client.generate_response_with_image(modelo, mensaje, ...)
    st.write(respuesta)
```

### Ejemplo 2: Extracción de texto (OCR)

Similar al ejemplo anterior, pero con un prompt específico para OCR:

```python
mensaje = [
    {"type": "text", "text": "Extrae todo el texto visible en esta imagen."},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}}
]
```

## Consideraciones de rendimiento

### Impacto en la memoria

- La codificación base64 aumenta el uso de memoria aproximadamente un 33%
- Las imágenes grandes pueden consumir recursos significativos

### Optimizaciones implementadas

1. **Procesamiento por lotes**:
   - Liberación de memoria después de cada procesamiento
   - Uso de contexto temporal para grandes operaciones

2. **Almacenamiento inteligente**:
   - Guardado selectivo de imágenes procesadas
   - Limpieza automática de archivos temporales

3. **Compresión adaptativa**:
   - Ajuste dinámico de la calidad según el tamaño
   - Priorización de la relación calidad/tamaño

## Conclusión

El uso de base64 para el procesamiento de imágenes en MetanoIA es una solución técnica necesaria que permite la integración de capacidades multimodales sin depender de servicios externos. Aunque presenta desafíos en términos de tamaño y eficiencia, las optimizaciones implementadas garantizan una experiencia fluida para el usuario mientras se mantiene la compatibilidad con las APIs de modelos de lenguaje.

Este enfoque no solo resuelve los requisitos técnicos inmediatos, sino que también establece una base sólida para futuras expansiones de las capacidades de visión en el proyecto, manteniendo siempre el enfoque educativo y transparente que caracteriza a MetanoIA.
