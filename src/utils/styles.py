"""
Módulo para la gestión de estilos y temas de la aplicación.
"""
import streamlit as st

def apply_fresh_tech_theme():
    """
    Aplica el tema "Fresh Tech" a la aplicación con gradientes y efectos modernos.
    """
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
