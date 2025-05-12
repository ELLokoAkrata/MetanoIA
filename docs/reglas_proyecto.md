# Reglas del Proyecto MetanoIA

**Fecha de creación**: 2025-05-11
**Última actualización**: 2025-05-11

## Principios Fundamentales

MetanoIA es un proyecto educativo de código abierto que busca enseñar una nueva forma de programar con inteligencia artificial. El objetivo principal es formar desarrolladores que comprendan a profundidad lo que construyen, aunque no programen de manera tradicional.

## Estructura del Proyecto

### Organización de Carpetas

```
MetanoIA/
├── app.py                 # Punto de entrada principal de la aplicación
├── docs/                  # Documentación del proyecto
│   ├── process.md         # Registro cronológico del proceso
│   ├── grimorio-proyecto.md # Compendio de información del proyecto
│   └── problemas_y_propuestas.md # Problemas detectados y soluciones
├── src/                   # Código fuente
│   ├── api/               # Integraciones con APIs externas
│   ├── components/        # Componentes de la interfaz de usuario
│   ├── models/            # Modelos y lógica de negocio
│   └── utils/             # Utilidades y herramientas auxiliares
├── tareas_diarias/        # Registro y planificación de tareas diarias
└── temp_images/           # Almacenamiento temporal de imágenes
```

## Procedimientos Estándar

### 1. Inicio de Sesión Diaria

Al comenzar cada sesión de trabajo:

1. **Revisar tareas pendientes**: Consultar `tareas_diarias/pendientes.md`
2. **Crear registro diario**: Generar un nuevo archivo en `tareas_diarias/YYYY-MM-DD.md`
3. **Actualizar process.md**: Añadir entrada con fecha y resumen de objetivos

### 2. Implementación de Nuevas Funcionalidades

Para cada nueva funcionalidad:

1. **Análisis preliminar**:
   - Revisar documentación existente
   - Identificar componentes relacionados
   - Crear documento de integración en `docs/integracion_[funcionalidad].md`

2. **Desarrollo**:
   - Seguir estructura de carpetas existente
   - Mantener separación de responsabilidades
   - Documentar cada función/clase con docstrings explicativos

3. **Documentación**:
   - Actualizar `grimorio-proyecto.md` con la nueva funcionalidad
   - Registrar proceso en `process.md`
   - Documentar problemas encontrados en `problemas_y_propuestas.md`

### 3. Resolución de Problemas

Cuando se encuentre un problema:

1. **Documentar el problema**:
   - Descripción clara del problema
   - Contexto en el que ocurre
   - Capturas de error si aplica

2. **Análisis sistemático**:
   - Revisar componentes relacionados
   - Identificar posibles causas
   - Proponer soluciones alternativas

3. **Implementación de solución**:
   - Documentar cambios realizados
   - Explicar razonamiento detrás de la solución
   - Crear archivo `docs/solucion_[problema].md` si es significativo

## Patrones de Código

### Estructura de Componentes

Los componentes siguen una estructura consistente:

```python
# Imports
import streamlit as st
from typing import Dict, List, Any

# Configuración de logging
import logging
logger = logging.getLogger(__name__)

class ComponentName:
    """
    Descripción detallada del componente y su propósito.
    
    Attributes:
        attribute_name: Descripción del atributo
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el componente con la configuración proporcionada.
        
        Args:
            config: Diccionario con la configuración del componente
        """
        self.config = config
        # Inicialización de otros atributos
        
    def render(self):
        """
        Renderiza el componente en la interfaz de Streamlit.
        
        Returns:
            Cualquier valor que deba ser retornado por el componente
        """
        # Implementación de la renderización
```

### Integración con APIs

Las integraciones con APIs siguen este patrón:

```python
# Imports
import requests
from typing import Dict, Any, Optional

class APIIntegration:
    """
    Descripción de la integración con la API.
    
    Attributes:
        base_url: URL base de la API
        api_key: Clave de API para autenticación
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Inicializa la integración con la API.
        
        Args:
            api_key: Clave de API para autenticación
            base_url: URL base opcional, usa el valor por defecto si no se proporciona
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.default.com"
        
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None):
        """
        Realiza una solicitud a la API.
        
        Args:
            endpoint: Endpoint específico de la API
            method: Método HTTP a utilizar
            data: Datos a enviar en la solicitud
            
        Returns:
            Respuesta de la API procesada
        """
        # Implementación de la solicitud
        
    def specific_operation(self, param1: str, param2: int):
        """
        Realiza una operación específica con la API.
        
        Args:
            param1: Descripción del parámetro 1
            param2: Descripción del parámetro 2
            
        Returns:
            Resultado de la operación
        """
        # Implementación de la operación específica
```

## Reglas de Comunicación

1. **Claridad sobre complejidad**: Explicar conceptos de manera clara y accesible
2. **Preguntas antes que suposiciones**: Preguntar cuando no se tenga certeza en lugar de suponer
3. **Documentación continua**: Documentar decisiones y razonamientos en tiempo real
4. **Feedback explícito**: Proporcionar retroalimentación clara sobre lo que funciona y lo que no

## Verificación de Calidad

Antes de considerar completa una tarea:

1. **Revisión de código**: ¿El código sigue los patrones establecidos?
2. **Documentación**: ¿Está todo documentado adecuadamente?
3. **Pruebas manuales**: ¿La funcionalidad trabaja como se espera?
4. **Integración**: ¿Se integra correctamente con el resto del sistema?
5. **Educación**: ¿El proceso y resultado son comprensibles para el usuario?

## Actualización de Reglas

Este documento debe revisarse y actualizarse regularmente para reflejar la evolución del proyecto y las lecciones aprendidas. Cualquier modificación debe registrarse con fecha y justificación.
