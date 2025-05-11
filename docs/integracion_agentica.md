# Integración de Capacidades Agénticas en MetanoIA

## Estado: Implementado (v1.0 - Mayo 2025)

Este documento describe la implementación de capacidades agénticas en MetanoIA, permitiendo que el sistema busque información en internet y ejecute código Python para proporcionar respuestas más precisas y actualizadas.

## Índice

1. [Modelos Compatibles](#modelos-compatibles)
2. [Capacidades Implementadas](#capacidades-implementadas)
3. [Arquitectura](#arquitectura)
4. [Integración con el Contexto](#integración-con-el-contexto)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
7. [Próximos Pasos](#próximos-pasos)

## Modelos Compatibles

Actualmente, se han integrado los siguientes modelos agénticos de Groq:

- **compound-beta**: Modelo principal con capacidades agénticas completas
- **compound-beta-mini**: Versión más ligera del modelo agéntico

Estos modelos permiten realizar tareas como:
- Búsqueda de información en internet en tiempo real
- Ejecución de código Python para cálculos y análisis
- Integración automática de los resultados en el contexto de la conversación

## Capacidades Implementadas

### 1. Búsqueda Web

Los modelos agénticos pueden buscar información en internet para responder preguntas sobre:
- Eventos actuales y noticias recientes
- Datos técnicos y científicos
- Información general que requiere conocimientos actualizados

La implementación incluye:
- Configuración de profundidad de búsqueda (básica o avanzada)
- Control del número máximo de resultados
- Filtrado por dominios a incluir o excluir
- Integración automática de las fuentes en las respuestas

### 2. Ejecución de Código

Los modelos pueden ejecutar código Python para:
- Realizar cálculos matemáticos complejos
- Analizar datos y generar estadísticas
- Crear visualizaciones y gráficos
- Implementar algoritmos y soluciones técnicas

## Arquitectura

La implementación de capacidades agénticas sigue una arquitectura modular:

### 1. Modelos Agénticos

```python
# src/models/agentic_models.py
class CompoundBetaModel(BaseLanguageModel):
    """Modelo Compound Beta de Groq con capacidades agénticas."""
    
    @property
    def id(self):
        return "compound-beta"
    
    @property
    def display_name(self):
        return "Compound Beta (Agéntico)"
    
    @property
    def is_agentic(self):
        return True
    
    @property
    def supports_multiple_tools(self):
        return True
```

### 2. Gestor de Herramientas Agénticas

```python
# src/utils/agentic_tools_manager.py
class AgenticToolsManager:
    """Gestor de herramientas agénticas para MetanoIA."""
    
    def __init__(self, session_state):
        self.session_state = session_state
        self.logger = setup_logger("AgenticTools")
    
    def process_executed_tools(self, executed_tools):
        """Procesa las herramientas ejecutadas por el modelo."""
        for tool in executed_tools:
            try:
                # Verificar que tool sea un diccionario
                if not isinstance(tool, dict):
                    continue
                
                # Obtener tipo de herramienta
                tool_type = tool.get("type")
                
                # Procesar según el tipo
                if tool_type == "search":
                    self._process_search_tool(tool)
                elif tool_type == "code_execution":
                    self._process_code_execution_tool(tool)
            except Exception as e:
                self.logger.error(f"Error al procesar herramienta: {str(e)}")
```

### 3. Integración en el Cliente de API

```python
# src/api/groq_client.py (extracto)
def generate_streaming_response(self, model, messages, temperature, max_tokens, callback=None):
    # ...
    
    # Procesar la respuesta (ahora puede ser un diccionario con content y executed_tools)
    if isinstance(response, dict):
        content = response.get("content", "")
        executed_tools = response.get("executed_tools", [])
        
        # Procesar herramientas ejecutadas si hay un gestor de herramientas agénticas
        if agentic_tools_manager and executed_tools:
            agentic_tools_manager.process_executed_tools(executed_tools)
```

## Integración con el Contexto

Las capacidades agénticas se integran con el contexto de conversación existente:

1. **Estado de Sesión Extendido**:
   ```python
   # src/utils/session_state.py
   if "agentic_context" not in st.session_state:
       st.session_state.agentic_context = {
           "search_results": [],
           "code_executions": [],
           "search_settings": {
               "search_depth": "basic",
               "max_results": 3,
               "include_domains": [],
               "exclude_domains": []
           }
       }
   ```

2. **Configuración en la Interfaz**:
   ```python
   # src/components/sidebar.py
   # Activar/desactivar herramientas agénticas
   enable_agentic = st.checkbox(
       "Activar herramientas agénticas",
       value=session_state.context.get("enable_agentic", False),
       help="Permite que el modelo busque información en internet y ejecute código Python."
   )
   
   # Configuración de búsqueda web
   if enable_agentic:
       st.subheader("Configuración de Búsqueda Web")
       # Configuración detallada...
   ```

## Ejemplos de Uso

### Búsqueda Web

Cuando el usuario hace una pregunta sobre información actualizada:

```
Usuario: ¿Cuáles son las últimas noticias sobre inteligencia artificial?
```

El modelo puede buscar en internet y responder con información actualizada, citando las fuentes utilizadas.

### Ejecución de Código

Para resolver problemas matemáticos o técnicos:

```
Usuario: ¿Puedes calcular la secuencia de Fibonacci hasta el número 100?
```

El modelo puede generar y ejecutar código Python para calcular la secuencia y mostrar los resultados.

## Limitaciones y Consideraciones

1. **Seguridad**:
   - La ejecución de código está limitada a operaciones seguras
   - No se permiten operaciones que puedan dañar el sistema o acceder a recursos sensibles

2. **Precisión**:
   - La información obtenida de internet puede no ser siempre precisa o actualizada
   - Los resultados de búsqueda dependen de la calidad de las fuentes disponibles

3. **Rendimiento**:
   - Las operaciones agénticas pueden aumentar el tiempo de respuesta
   - Búsquedas complejas o ejecuciones de código intensivas pueden requerir más tiempo

## Próximos Pasos

Para futuras versiones, se planean las siguientes mejoras:

1. **Expansión de herramientas**:
   - Integración con APIs externas específicas
   - Capacidades para interactuar con bases de datos
   - Herramientas para análisis de datos más avanzados

2. **Mejoras de seguridad**:
   - Implementación de un sandbox más robusto para ejecución de código
   - Controles más granulares para las operaciones permitidas

3. **Personalización**:
   - Permitir al usuario definir sus propias herramientas
   - Configuración avanzada de preferencias de búsqueda

## Conclusión

La integración de capacidades agénticas en MetanoIA representa un avance significativo en la funcionalidad del asistente, permitiéndole acceder a información actualizada y realizar tareas complejas en tiempo real. Esta implementación mantiene el enfoque educativo del proyecto, proporcionando no solo respuestas más precisas, sino también transparencia en el proceso de obtención y procesamiento de la información.
