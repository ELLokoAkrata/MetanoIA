### 2025-05-11: Error en la API de transcripción de audio de Groq
**Problema**: Al intentar utilizar la API de transcripción de audio de Groq, se produjo un error de compatibilidad con la biblioteca actual:

```
Traceback (most recent call last):
  File "C:\Users\Ricardo Ruiz\Desktop\MetanoIA\src\api\audio_transcription.py", line 64, in transcribe_audio
    transcription = client.audio.transcriptions.create(**params)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\resources\audio\transcriptions.py", line 120, in create
    self._post(
  File "C:\Python311\Lib\site-packages\groq\_base_client.py", line 1225, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_base_client.py", line 920, in request
    return self._request(
           ^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_base_client.py", line 1020, in _request
    return self._process_response(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_base_client.py", line 1101, in _process_response
    return api_response.parse()
           ^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_response.py", line 303, in parse
    parsed = self._parse(to=to)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_response.py", line 223, in _parse
    if is_basemodel(cast_to):
       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_models.py", line 374, in is_basemodel
    return is_basemodel_type(type_)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\groq\_models.py", line 379, in is_basemodel_type
    return issubclass(origin, BaseModel) or issubclass(origin, GenericModel)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen abc>", line 123, in __subclasscheck__
TypeError: issubclass() arg 1 must be a class
```

**Impacto**: No es posible utilizar la funcionalidad de transcripción de audio de Groq directamente a través de la biblioteca de Python, lo que limita la capacidad multimodal de la aplicación para procesar entradas de voz.

**Solución implementada**: Se modificó el código para utilizar directamente los endpoints de la API de Groq mediante solicitudes HTTP en lugar de depender de la funcionalidad específica de audio de la biblioteca de Groq:

```python
# Implementación directa usando requests en lugar de la biblioteca de Groq
def transcribe_audio(self, audio_path, model="whisper-large-v3-turbo", language=None, response_format="text"):
    # ...
    # Obtener la clave API del cliente de Groq
    api_key = self.groq_client.api_key
    
    # Preparar los headers para la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Preparar los datos para la solicitud
    files = {
        "file": (os.path.basename(audio_path), open(audio_path, "rb"))
    }
    
    data = {
        "model": model,
        "response_format": response_format
    }
    
    # Añadir parámetros opcionales si están presentes
    if language:
        data["language"] = language
    
    # Realizar la solicitud HTTP directamente al endpoint de transcripción
    response = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers=headers,
        files=files,
        data=data
    )
```

**Estado**: ✅ Implementado
