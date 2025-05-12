# Integración de Generación de Archivos con Tool-Use de Groq

**Fecha de creación**: 2025-05-12

## Descripción

Esta integración permite a MetanoIA generar archivos en diferentes formatos (JSON, Python, Markdown y TXT) utilizando la funcionalidad de Tool-Use de Groq, y proporciona un botón para descargar estos archivos directamente desde la interfaz.

## Modelos compatibles

La funcionalidad de Tool-Use está disponible en los siguientes modelos de Groq:

- `meta-llama/llama-4-scout-17b-16e-instruct`
- `meta-llama/llama-4-maverick-17b-128e-instruct`
- `qwen-qwq-32b`
- `deepseek-r1-distill-qwen-32b`
- `deepseek-r1-distill-llama-70b`
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `gemma2-9b-it`

Para esta implementación, utilizaremos principalmente `llama-3.3-70b-versatile` por su buen equilibrio entre rendimiento y capacidad.

## Arquitectura

La integración se compone de los siguientes elementos:

1. **API Client**: Extensión del cliente de Groq para soportar llamadas con herramientas (tools).
2. **Herramientas de generación**: Definición de herramientas para generar archivos en diferentes formatos.
3. **Componente de UI**: Interfaz para solicitar la generación de archivos y mostrar botones de descarga.
4. **Gestor de archivos**: Manejo de archivos temporales y descarga.

## Flujo de trabajo

1. El usuario solicita la generación de un archivo en un formato específico.
2. La aplicación envía la solicitud al modelo con las herramientas definidas.
3. El modelo decide qué herramienta utilizar y genera el contenido del archivo.
4. La aplicación guarda el archivo generado temporalmente.
5. Se muestra un botón de descarga para que el usuario obtenga el archivo.

## Implementación técnica

### 1. Extensión del cliente de Groq

Extenderemos el cliente de Groq existente para soportar llamadas con herramientas:

```python
def generate_response_with_tools(self, model, messages, tools, temperature, max_tokens, callback=None):
    """
    Genera una respuesta utilizando herramientas definidas.
    
    Args:
        model (str): ID del modelo a utilizar.
        messages (list): Lista de mensajes para la conversación.
        tools (list): Lista de herramientas disponibles.
        temperature (float): Temperatura para la generación.
        max_tokens (int): Número máximo de tokens en la respuesta.
        callback (callable, optional): Función de callback para cada fragmento de respuesta.
        
    Returns:
        dict: Diccionario con la respuesta y las llamadas a herramientas.
    """
    # Implementación
```

### 2. Definición de herramientas

Definiremos herramientas para generar diferentes tipos de archivos:

```python
# Herramienta para generar archivos JSON
json_generator_tool = {
    "type": "function",
    "function": {
        "name": "generate_json",
        "description": "Genera un archivo JSON basado en la solicitud del usuario",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "object",
                    "description": "El contenido del archivo JSON"
                },
                "filename": {
                    "type": "string",
                    "description": "Nombre del archivo a generar (sin extensión)"
                }
            },
            "required": ["content", "filename"]
        }
    }
}

# Herramientas similares para Python, Markdown y TXT
```

### 3. Implementación de funciones de generación

```python
def generate_json_file(content, filename):
    """
    Genera un archivo JSON y devuelve la ruta para descarga.
    
    Args:
        content (dict): Contenido del archivo JSON.
        filename (str): Nombre del archivo sin extensión.
        
    Returns:
        str: Ruta al archivo generado.
    """
    # Implementación
```

### 4. Componente de UI para descarga

```python
def display_file_download(file_path, file_type):
    """
    Muestra un botón para descargar el archivo generado.
    
    Args:
        file_path (str): Ruta al archivo generado.
        file_type (str): Tipo de archivo (json, py, md, txt).
    """
    # Implementación
```

## Consideraciones

1. **Seguridad**: Validar el contenido generado antes de guardarlo.
2. **Limpieza**: Implementar un sistema para eliminar archivos temporales.
3. **Feedback**: Proporcionar información clara sobre el proceso de generación.
4. **Errores**: Manejar adecuadamente los errores y proporcionar mensajes útiles.

## Ejemplos de uso

### Generar un archivo JSON

```
Usuario: "Genera un archivo JSON con información de 3 libros de ciencia ficción"
```

### Generar un script Python

```
Usuario: "Crea un script Python que calcule números primos"
```

## Implementación realizada

### 1. Extensión del cliente de Groq

Se ha implementado el método `generate_response_with_tools` en la clase `GroqClient` para soportar llamadas con herramientas:

```python
def generate_response_with_tools(self, model, messages, tools, temperature, max_tokens, callback=None, tool_choice="auto"):
    """Genera una respuesta utilizando herramientas definidas."""
    try:
        # Configurar el cliente de Groq
        client = Groq(api_key=self.api_key)
        
        # Registrar la solicitud
        logger.info(f"Generando respuesta con herramientas usando modelo: {model}")
        
        # Realizar la llamada a la API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice
        )
        
        # Procesar la respuesta
        result = {
            "content": response.choices[0].message.content or "",
            "tool_calls": []
        }
        
        # Extraer las llamadas a herramientas si existen
        if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                if tool_call.type == "function":
                    result["tool_calls"].append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
        
        return result
    except Exception as e:
        logger.error(f"Error al generar respuesta con herramientas: {str(e)}")
        raise
```

### 2. Implementación del generador de archivos

Se ha creado la clase `FileGenerator` en el módulo `src/api/file_generator.py` para manejar la generación de archivos:

```python
class FileGenerator:
    """Clase para generar archivos usando herramientas de LLM."""
    
    def __init__(self, temp_dir):
        """Inicializa el generador de archivos."""
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
    
    def get_tools_definitions(self) -> List[Dict[str, Any]]:
        """Devuelve las definiciones de herramientas para generación de archivos."""
        return [
            # Definiciones para JSON, Python, Markdown y TXT
        ]
    
    def generate_json_file(self, content: str, filename: str = None) -> str:
        """Genera un archivo JSON."""
        if filename is None or not filename.strip():
            filename = f"generated_{int(time.time())}.json"
        elif not filename.endswith(".json"):
            filename = f"{filename}.json"
            
        file_path = os.path.join(self.temp_dir, filename)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return file_path
        except Exception as e:
            logger.error(f"Error al generar archivo JSON: {str(e)}")
            raise
    
    # Métodos similares para Python, Markdown y TXT
```

### 3. Componente UI para generación y descarga

Se ha implementado el componente `FileGeneratorUI` en `src/components/file_generator.py`:

```python
class FileGeneratorUI:
    """Componente UI para la generación y descarga de archivos."""
    
    def __init__(self, file_generator: FileGenerator, groq_client: GroqClient):
        """Inicializa el componente UI."""
        self.file_generator = file_generator
        self.groq_client = groq_client
    
    def display_file_download(self, file_path: str, file_type: str):
        """Muestra un botón para descargar el archivo generado."""
        if not os.path.exists(file_path):
            st.error(f"El archivo {file_path} no existe.")
            return
            
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            
        st.code(file_content, language=file_type)
        
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"Descargar {filename}",
                data=f,
                file_name=filename,
                mime=self._get_mime_type(file_type)
            )
    
    def _get_mime_type(self, file_type: str) -> str:
        """Devuelve el tipo MIME para el tipo de archivo."""
        mime_types = {
            "json": "application/json",
            "py": "text/x-python",
            "md": "text/markdown",
            "txt": "text/plain"
        }
        return mime_types.get(file_type, "text/plain")
```

## Lecciones aprendidas

### 1. Estructura de mensajes consistente

Es crucial mantener una estructura de mensajes consistente en toda la aplicación. Durante la implementación, encontramos problemas debido a discrepancias entre cómo se guardaban los mensajes en diferentes componentes (usando `is_user` vs. `role`). La solución fue implementar funciones que pudieran manejar ambos formatos para garantizar la compatibilidad.

### 2. Gestión centralizada de archivos temporales

Centralizar la gestión de archivos temporales en un solo módulo (`session_state.py`) facilita el mantenimiento y evita la duplicación de código. Esto también asegura que los archivos se limpien correctamente cuando la sesión finaliza.

### 3. Manejo de errores robusto

Implementar un manejo de errores robusto es esencial para proporcionar una buena experiencia de usuario. Capturar y registrar excepciones específicas permite identificar y solucionar problemas rápidamente.

### 4. Compatibilidad con modelos

No todos los modelos soportan Tool-Use de la misma manera. Es importante verificar la compatibilidad y ajustar la implementación según sea necesario. El modelo `llama-3.3-70b-versatile` ha demostrado ser particularmente efectivo para esta funcionalidad.

## Próximas mejoras

1. **Plantillas predefinidas**: Implementar plantillas para tipos comunes de archivos que los usuarios puedan personalizar.
2. **Edición colaborativa**: Permitir la edición de archivos generados antes de descargarlos.
3. **Más formatos**: Expandir la funcionalidad para soportar más formatos como CSV, HTML, CSS, etc.
4. **Validación mejorada**: Implementar validación más robusta para garantizar que los archivos generados sean válidos y seguros.
5. **Integración con sistemas de control de versiones**: Permitir guardar los archivos generados directamente en repositorios Git.
