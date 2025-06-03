"""Utilidades para procesar texto en archivos."""

from typing import Callable, List, Dict, Any
import re
import json
import io

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover - dependency opcional
    PdfReader = None


def tokenize_text(text: str) -> List[str]:
    """Divide el texto en tokens usando espacios y puntuación como separadores.

    Args:
        text: Texto a tokenizar.

    Returns:
        Lista de tokens encontrados.
    """
    # Usamos una expresión regular sencilla para separar palabras y signos
    return re.findall(r"\w+|[^\w\s]", text)


def split_text_by_tokens(text: str, max_tokens: int, tokenizer: Callable[[str], List[str]] | None = None) -> List[str]:
    """Divide un texto en partes que no excedan un número de tokens.

    Args:
        text: Texto completo a dividir.
        max_tokens: Número máximo de tokens por parte.
        tokenizer: Función opcional para convertir texto en tokens.

    Returns:
        Lista de fragmentos de texto.
    """
    tokenizer = tokenizer or tokenize_text
    tokens = tokenizer(text)

    chunks: List[str] = []
    current: List[str] = []

    for token in tokens:
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []
        current.append(token)

    if current:
        chunks.append(" ".join(current))

    return chunks


def summarize_text(text: str, max_tokens: int, tokenizer: Callable[[str], List[str]] | None = None) -> str:
    """Resume el texto si supera el número máximo de tokens especificado.

    El resumen consiste en truncar el texto y añadir una indicación final.

    Args:
        text: Texto a resumir.
        max_tokens: Número máximo de tokens permitidos.
        tokenizer: Función opcional para convertir texto en tokens.

    Returns:
        Texto original o resumido si excede el límite.
    """
    tokenizer = tokenizer or tokenize_text
    tokens = tokenizer(text)

    if len(tokens) <= max_tokens:
        return text

    summary_tokens = tokens[:max_tokens]
    return " ".join(summary_tokens) + " ..."


def read_text(content: bytes | str) -> str:
    """Lee datos de texto y los decodifica a una cadena."""

    if isinstance(content, bytes):
        return content.decode("utf-8", errors="ignore")
    return content


def read_json(content: bytes | str) -> Dict[str, Any]:
    """Convierte datos JSON a un diccionario."""

    text = read_text(content)
    return json.loads(text)


def read_pdf(content: bytes) -> str:
    """Extrae texto de un PDF utilizando ``PyPDF2``.

    Args:
        content: Datos binarios del PDF.

    Returns:
        Texto extraído del PDF.

    Raises:
        ImportError: Si ``PyPDF2`` no está disponible.
    """

    if PdfReader is None:
        raise ImportError("PyPDF2 es necesario para leer archivos PDF")

    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text.strip()
