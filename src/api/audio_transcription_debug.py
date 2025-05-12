"""
Archivo temporal para depurar la respuesta de la API de transcripción de audio de Groq.
"""

import os
import time
import requests
import json

# Función para depurar la respuesta de la API
def debug_transcription_response(api_key, audio_path, model="whisper-large-v3-turbo", language="es"):
    """
    Depura la respuesta de la API de transcripción de audio de Groq.
    
    Args:
        api_key (str): Clave API de Groq.
        audio_path (str): Ruta al archivo de audio.
        model (str): Modelo de Whisper a utilizar.
        language (str): Código de idioma.
    """
    print(f"Iniciando depuración de transcripción para: {os.path.basename(audio_path)}")
    print(f"Modelo: {model}, Idioma: {language}")
    
    start_time = time.time()
    
    # Preparar los headers para la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Preparar los datos para la solicitud
    files = {
        "file": (os.path.basename(audio_path), open(audio_path, "rb"))
    }
    
    # Probar con diferentes formatos de respuesta
    formats = ["text", "json", "verbose_json"]
    results = {}
    
    for fmt in formats:
        print(f"\nProbando con formato: {fmt}")
        
        data = {
            "model": model,
            "response_format": fmt
        }
        
        if language:
            data["language"] = language
        
        # Realizar la solicitud HTTP
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data=data
            )
            
            print(f"Código de estado: {response.status_code}")
            print(f"Tipo de contenido: {response.headers.get('Content-Type', 'desconocido')}")
            
            if response.status_code == 200:
                if fmt in ["json", "verbose_json"]:
                    try:
                        json_data = response.json()
                        print(f"Respuesta JSON: {json.dumps(json_data, indent=2, ensure_ascii=False)[:500]}...")
                        results[fmt] = json_data
                    except Exception as e:
                        print(f"Error al procesar JSON: {str(e)}")
                        print(f"Contenido de la respuesta: {response.text[:500]}...")
                else:
                    print(f"Respuesta texto: {response.text[:500]}...")
                    results[fmt] = response.text
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Excepción: {str(e)}")
    
    elapsed_time = time.time() - start_time
    print(f"\nDepuración completada en {elapsed_time:.2f} segundos")
    
    return results

# Uso:
# debug_transcription_response("tu_api_key", "ruta/al/archivo.wav")
