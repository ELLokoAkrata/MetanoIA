# Verificación de la Integración del Procesamiento de Archivos

## Introducción

Este documento proporciona una guía para verificar la correcta integración y funcionamiento del sistema de procesamiento de archivos en MetanoIA. Incluye pruebas manuales y automáticas para validar cada componente y su interacción con el resto del sistema.

## Pruebas Manuales

### 1. Verificación de la Interfaz de Usuario

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| Carga del componente | 1. Iniciar la aplicación<br>2. Verificar que aparece el componente de subida de archivos | El componente se muestra correctamente en la interfaz | ⏳ |
| Subida de archivo | 1. Hacer clic en el área de subida<br>2. Seleccionar un archivo TXT<br>3. Verificar que se muestra el nombre del archivo | El archivo se carga y se muestra su nombre | ⏳ |
| Detección de tipo | 1. Subir archivos de diferentes tipos (TXT, JSON, PDF)<br>2. Verificar que se detecta correctamente el tipo | Se muestra el tipo de archivo correcto para cada uno | ⏳ |
| Procesamiento | 1. Subir un archivo<br>2. Hacer clic en "Procesar"<br>3. Verificar que se muestra el resultado | El archivo se procesa y se muestra el resultado | ⏳ |
| Integración con chat | 1. Procesar un archivo<br>2. Verificar que el contenido se añade al historial de chat | Se añade un mensaje del sistema con información del archivo | ⏳ |

### 2. Verificación de Funcionalidad por Tipo de Archivo

#### Archivos de Texto (TXT)

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| Archivo pequeño | Procesar un TXT de menos de 1000 caracteres | Se procesa completo sin fragmentación | ⏳ |
| Archivo grande | Procesar un TXT de más de 10000 caracteres | Se fragmenta y se genera un resumen | ⏳ |
| Codificación UTF-8 | Procesar un TXT con caracteres especiales | Se mantienen los caracteres especiales | ⏳ |

#### Archivos JSON

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| JSON simple | Procesar un JSON con estructura simple | Se convierte correctamente a diccionario | ⏳ |
| JSON complejo | Procesar un JSON con estructuras anidadas | Se mantiene la estructura jerárquica | ⏳ |
| JSON inválido | Procesar un archivo con formato JSON inválido | Se muestra un error apropiado | ⏳ |

#### Archivos PDF

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| PDF de texto | Procesar un PDF que contiene principalmente texto | Se extrae el texto correctamente | ⏳ |
| PDF con imágenes | Procesar un PDF con imágenes y texto | Se extrae el texto ignorando las imágenes | ⏳ |
| PDF protegido | Procesar un PDF con restricciones | Se muestra un error apropiado | ⏳ |

### 3. Verificación de Gestión de Estado

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| Inicialización | Verificar que `processed_files` se inicializa en `session_state` | La lista existe y está vacía al inicio | ⏳ |
| Actualización | Procesar un archivo y verificar que se añade a `processed_files` | El archivo procesado aparece en la lista | ⏳ |
| Limpieza | Cerrar la sesión y verificar que se eliminan los archivos temporales | No quedan archivos temporales en el sistema | ⏳ |

## Pruebas Automáticas

Se recomienda implementar las siguientes pruebas automáticas para validar la integración:

```python
def test_file_processor_initialization():
    """Prueba que FileProcessor se inicializa correctamente."""
    processor = FileProcessor()
    assert processor is not None
    assert hasattr(processor, 'process_file')

def test_txt_processing():
    """Prueba el procesamiento de archivos TXT."""
    processor = FileProcessor()
    with open('test_files/sample.txt', 'r') as f:
        content = f.read()
    result = processor.process_file(content, 'txt')
    assert result['success'] is True
    assert 'content' in result
    assert 'summary' in result

def test_json_processing():
    """Prueba el procesamiento de archivos JSON."""
    processor = FileProcessor()
    with open('test_files/sample.json', 'r') as f:
        content = f.read()
    result = processor.process_file(content, 'json')
    assert result['success'] is True
    assert 'content' in result
    assert isinstance(result['content'], dict)

def test_session_state_integration():
    """Prueba la integración con el estado de sesión."""
    # Simular estado de sesión
    session_state = {'processed_files': []}
    
    # Procesar archivo
    processor = FileProcessor()
    result = processor.process_file("Test content", 'txt')
    
    # Actualizar estado de sesión
    session_state['processed_files'].append({
        'file_name': 'test.txt',
        'file_type': 'txt',
        'content': result['content'],
        'summary': result.get('summary', '')
    })
    
    assert len(session_state['processed_files']) == 1
    assert session_state['processed_files'][0]['file_type'] == 'txt'
```

## Verificación de Integración con Componentes Existentes

### 1. Integración con Generación de Archivos

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| Flujo completo | 1. Procesar un archivo<br>2. Generar un nuevo archivo basado en el procesado<br>3. Descargar el archivo generado | El flujo completo funciona sin errores | ⏳ |
| Compartir utilidades | Verificar que ambos componentes utilizan las mismas utilidades de `file_utils.py` | No hay duplicación de código | ⏳ |

### 2. Integración con Sistema de Chat

| Prueba | Pasos | Resultado Esperado | Estado |
|--------|-------|-------------------|--------|
| Contexto de chat | Verificar que el contenido procesado se añade al contexto de chat | El modelo puede referenciar el contenido del archivo | ⏳ |
| Comandos de chat | Probar comandos como "resume este archivo" o "analiza este archivo" | El modelo responde apropiadamente a los comandos | ⏳ |

## Registro de Problemas y Soluciones

| Problema | Descripción | Solución | Estado |
|----------|------------|----------|--------|
| Ejemplo: Archivos temporales no se eliminan | Los archivos subidos no se eliminan al cerrar la sesión | Implementar limpieza en `cleanup_temp_files()` | ✅ |
| | | | |

## Conclusión

La verificación completa de la integración del procesamiento de archivos es esencial para garantizar una experiencia de usuario fluida y coherente. Este documento debe actualizarse a medida que se implementen nuevas funcionalidades o se resuelvan problemas existentes.

**Leyenda:**
- ✅ Completado
- 🔄 En progreso
- ⏳ Pendiente
