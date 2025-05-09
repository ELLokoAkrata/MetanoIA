import os
import streamlit as st
from groq import Groq
import time
import datetime
import logging

# Configurar sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("psycho-bot")

# Configuración de página
st.set_page_config(page_title="Psycho-bot", layout="wide", initial_sidebar_state="expanded")

# Aplicar CSS personalizado para tema "Fresh Tech"
st.markdown("""
<style>
/* Tema base con gradiente para toda la aplicación */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    color: #e2e8f0 !important;
}

/* Estilos para la barra lateral con gradiente */
.css-1d391kg, .css-1lcbmhc, .css-12oz5g7 {
    background: linear-gradient(180deg, #1e1e2f 0%, #2d2d44 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.2) !important;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.1) !important;
}

/* Estilos para widgets en la barra lateral */
.sidebar .stTextInput, .sidebar .stSelectbox, .sidebar .stSlider {
    background-color: rgba(30, 41, 59, 0.7) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    backdrop-filter: blur(5px) !important;
}

/* Estilos para botones con efecto de neón */
.stButton button {
    background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.5) !important;
}

.stButton button:hover {
    background: linear-gradient(90deg, #6366f1 0%, #818cf8 100%) !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.7) !important;
    transform: translateY(-2px) !important;
}

/* Estilos para contenedores */
div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

/* Estilos para mensajes de chat con efecto de vidrio */
.stChatMessage {
    background-color: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
}

/* Estilos específicos para mensajes de usuario y asistente */
.stChatMessage[data-testid="user"] {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%) !important;
    border-left: 5px solid #38bdf8 !important;
}

.stChatMessage[data-testid="assistant"] {
    background: linear-gradient(135deg, rgba(134, 239, 172, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%) !important;
    border-left: 5px solid #86efac !important;
}

/* Estilos para texto en toda la aplicación */
p, div, span, label, .stMarkdown, .stText {
    color: #e2e8f0 !important;
}

/* Estilos para títulos con gradiente */
h1 {
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 700 !important;
}

h2, h3, h4, h5, h6 {
    color: #e2e8f0 !important;
}

/* Estilos para entrada de chat */
.stChatInput > div {
    background-color: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(5px) !important;
}

.stChatInput input {
    color: #e2e8f0 !important;
}

/* Estilos para selectbox */
.stSelectbox > div > div {
    background-color: rgba(30, 41, 59, 0.7) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 8px !important;
}

/* Estilos para sliders con colores vibrantes */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%) !important;
}

/* Estilos para textarea */
.stTextArea > div > div > textarea {
    background-color: rgba(30, 41, 59, 0.7) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(5px) !important;
}

/* Arreglar problemas con la barra lateral */
.css-1544g2n.e1fqkh3o4 {
    padding-top: 2rem !important;
    padding-right: 1rem !important;
    padding-left: 1rem !important;
    overflow-y: auto !important;
}

/* Estilos para scrollbars */
::-webkit-scrollbar {
    width: 8px;
    background-color: rgba(15, 23, 42, 0.3);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #4f46e5 0%, #6366f1 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #6366f1 0%, #818cf8 100%);
}

/* Efecto de brillo sutil en los bordes */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# --- Definición de modelos disponibles ---
models = {
    "deepseek-r1-distill-llama-70b": "DeepSeek (128K)",
    "meta-llama/llama-4-maverick-17b-128e-instruct": "Meta Maverick (131K)",
    "meta-llama/llama-4-scout-17b-16e-instruct": "Meta Scout (131K)",
    "qwen-qwq-32b": "Alibaba Qwen (128K)"
}

# --- Inicialización de variables de sesión ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = {
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.7,
        "max_tokens": 1024,
        "system_prompt": "Eres un asistente virtual amigable y útil."
    }

# --- Configuración de la barra lateral ---
with st.sidebar:
    st.title("⚙️ Configuración")
    
    # Configuración de la API
    st.subheader("API")
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            logger.info("API key configurada")
    
    # Selección de modelo
    st.subheader("Modelo")
    
    # Usar key para forzar la recreación del widget cuando cambia el modelo
    selected_model = st.selectbox(
        "Selecciona un modelo",
        options=list(models.keys()),
        format_func=lambda x: models[x],
        index=list(models.keys()).index(st.session_state.context["model"]) if st.session_state.context["model"] in models else 0,
        key=f"model_select_{st.session_state.context['model']}"
    )
    
    # Parámetros de generación
    st.subheader("Parámetros")
    temperature = st.slider(
        "Temperatura", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.context["temperature"],
        step=0.1,
        help="Controla la aleatoriedad de las respuestas. Valores más altos = más creatividad."
    )
    
    max_tokens = st.slider(
        "Máximo de tokens", 
        min_value=256, 
        max_value=4096, 
        value=st.session_state.context["max_tokens"],
        step=128,
        help="Número máximo de tokens en la respuesta."
    )
    
    # System prompt
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Instrucciones para el asistente",
        value=st.session_state.context["system_prompt"],
        height=150
    )
    
    # Actualizar contexto cuando cambian los valores
    if (selected_model != st.session_state.context["model"]):
        logger.info(f"Cambio de modelo: {st.session_state.context['model']} -> {selected_model}")
        st.session_state.context["model"] = selected_model
        # Forzar recarga para aplicar el cambio inmediatamente
        st.rerun()
    
    if (temperature != st.session_state.context["temperature"] or
        max_tokens != st.session_state.context["max_tokens"] or
        system_prompt != st.session_state.context["system_prompt"]):
        
        logger.info(f"Cambio de parámetros: temperatura={temperature}, max_tokens={max_tokens}")
        st.session_state.context["temperature"] = temperature
        st.session_state.context["max_tokens"] = max_tokens
        st.session_state.context["system_prompt"] = system_prompt
    
    # Botón para limpiar la conversación
    if st.button("Limpiar conversación"):
        logger.info("Conversación limpiada")
        st.session_state.messages = []
        st.rerun()

# --- Título principal ---
st.title("🤖 Bot simple configurable")
st.markdown("Chat bot usando Streamlit y la API de Groq")

# --- Función para llamar a la API con caché ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_response(model, messages_str, temperature, max_tokens):
    """Función cacheada para obtener respuestas que no cambiarán con los mismos parámetros"""
    try:
        logger.info(f"Llamada a API (caché) con modelo: {model}, temperatura: {temperature}, max_tokens: {max_tokens}")
        start_time = time.time()
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=eval(messages_str),  # Convertir string a lista de diccionarios
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"Respuesta recibida en {elapsed_time:.2f} segundos")
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error al llamar a la API: {str(e)}")
        return f"Error al llamar a la API: {str(e)}"

# --- Función para streaming de respuestas ---
def generate_streaming_response(model, messages, temperature, max_tokens):
    """Genera respuestas en streaming para una experiencia más interactiva"""
    try:
        # Registrar información sobre la llamada a la API
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{current_time}] Iniciando llamada a API (streaming) con modelo: {model}")
        logger.info(f"Parámetros: temperatura={temperature}, max_tokens={max_tokens}")
        
        # Mostrar mensaje de carga en la interfaz
        with st.spinner(f"Generando respuesta con {models.get(model, model)}..."):
            start_time = time.time()
            
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            logger.info(f"Conexión establecida, comenzando streaming...")
            
            response_placeholder = st.empty()
            full_response = ""
            chunk_count = 0
            
            for chunk in stream:
                chunk_count += 1
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)
                    time.sleep(0.01)  # Pequeña pausa para simular escritura
            
            elapsed_time = time.time() - start_time
            logger.info(f"Streaming completado: {chunk_count} chunks recibidos en {elapsed_time:.2f} segundos")
            
            return full_response
    except Exception as e:
        error_msg = f"Error al llamar a la API: {str(e)}"
        logger.error(error_msg)
        logger.exception("Detalles del error:")
        return error_msg

# --- Contenedor principal del chat ---
chat_container = st.container()

# --- Mostrar mensajes anteriores ---
with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        role_style = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(msg["role"]):
            # Si es un mensaje del asistente y tiene información del modelo usado, mostrarla
            if msg["role"] == "assistant" and "model_used" in msg:
                model_name = models.get(msg["model_used"], msg["model_used"])
                st.caption(f"Generado por: {model_name}")
            
            # Mostrar el contenido del mensaje
            st.markdown(msg["content"])

# --- Entrada de usuario ---
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Verificar que tenemos una API key
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Por favor, ingresa tu API key de Groq en la barra lateral.")
        st.stop()
    
    # Obtener el modelo actual directamente del contexto
    current_model = st.session_state.context["model"]
    logger.info(f"Usando modelo seleccionado: {current_model} ({models.get(current_model, 'Desconocido')})")
    
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # --- Preparar mensajes para la API (filtrando campos personalizados y limitando el contexto)
    api_messages = [
        {"role": "system", "content": st.session_state.context["system_prompt"]}
    ]
    
    # Obtener el número máximo de mensajes a incluir según el modelo
    # Esto evita exceder los límites de tokens por minuto (TPM)
    max_context_messages = 10  # Valor predeterminado
    
    # Ajustar el contexto según el modelo para evitar errores de límite de tokens
    if "llama-4-maverick" in current_model:
        max_context_messages = 5  # Limitar más para modelos que tienen límites más estrictos
    elif "llama-4-scout" in current_model:
        max_context_messages = 6
    
    # Registrar el límite de contexto aplicado
    logger.info(f"Limitando contexto a {max_context_messages} mensajes para el modelo {current_model}")
    
    # Añadir mensajes del historial filtrando campos personalizados y limitando la cantidad
    # Tomamos solo los mensajes más recientes para no exceder los límites
    recent_messages = st.session_state.messages[-max_context_messages:] if len(st.session_state.messages) > max_context_messages else st.session_state.messages
    
    for msg in recent_messages:
        if msg["role"] in ["user", "assistant"]:
            # Solo incluir campos estándar (role y content)
            api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        # Mostrar qué modelo se está usando
        model_info = st.empty()
        model_info.info(f"Generando respuesta con {models.get(current_model, current_model)}...")
        
        # Generar respuesta
        full_response = generate_streaming_response(
            model=current_model,  # Usar el modelo actual del contexto
            messages=api_messages,
            temperature=st.session_state.context["temperature"],
            max_tokens=st.session_state.context["max_tokens"]
        )
        
        # Eliminar el mensaje de información una vez completada la respuesta
        model_info.empty()
    
    # Agregar respuesta al historial con información del modelo usado
    model_used_info = f"[Generado por: {models.get(current_model, current_model)}]\n\n"
    st.session_state.messages.append({"role": "assistant", "content": full_response, "model_used": current_model})