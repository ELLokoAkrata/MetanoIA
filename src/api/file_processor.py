""" 
Módulo para leer archivos y prepararlos para su integración en el contexto.
"""

import json
import os
import re
from typing import Any, Dict, List

try:
    from PyPDF2 import PdfReader  # type: ignore
except ImportError:  # pragma: no cover - dependencia opcional
    PdfReader = None

from src.utils.logger import setup_logger


class FileProcessor:
    """Procesa archivos y los divide en fragmentos manejables."""

    def __init__(self, max_tokens: int = 1024, logger=None) -> None:
        """Inicializa el procesador de archivos.

        Args:
            max_tokens: Límite de tokens por fragmento.
            logger: Logger opcional para registrar información.
        """
        self.max_tokens = max_tokens
        self.logger = logger or setup_logger("FileProcessor")

    # Funciones de lectura -------------------------------------------------
    def _read_txt(self, file_path: str) -> str:
        """Lee un archivo de texto plano.

        Args:
            file_path: Ruta al archivo.

        Returns:
            Contenido del archivo como cadena.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_json(self, file_path: str) -> str:
        """Lee un archivo JSON y lo devuelve formateado.

        Args:
            file_path: Ruta al archivo.

        Returns:
            Cadena JSON formateada.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _read_pdf(self, file_path: str) -> str:
        """Lee un archivo PDF utilizando PyPDF2.

        Args:
            file_path: Ruta al archivo.

        Returns:
            Texto extraído del PDF.
        """
        if PdfReader is None:
            raise ImportError("PyPDF2 no está instalado")
        reader = PdfReader(file_path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    # Tokenización y fragmentación ----------------------------------------
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniza el texto de forma sencilla usando espacios."""
        return re.findall(r"\w+|[^\w\s]", text)

    def _split_tokens(self, tokens: List[str]) -> List[str]:
        """Divide la lista de tokens en fragmentos.

        Args:
            tokens: Lista de tokens.

        Returns:
            Lista de fragmentos como cadenas.
        """
        chunks: List[str] = []
        for i in range(0, len(tokens), self.max_tokens):
            chunk_tokens = tokens[i : i + self.max_tokens]
            chunks.append(" ".join(chunk_tokens))
        return chunks

    # API pública ----------------------------------------------------------
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """Carga un archivo, lo tokeniza y lo divide en fragmentos.

        Args:
            file_path: Ruta al archivo a procesar.

        Returns:
            Diccionario con el contenido completo, los fragmentos y metadatos.
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".txt":
            text = self._read_txt(file_path)
        elif ext == ".json":
            text = self._read_json(file_path)
        elif ext == ".pdf":
            text = self._read_pdf(file_path)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {ext}")

        tokens = self._tokenize(text)
        chunks = self._split_tokens(tokens)

        metadata = {
            "file_name": os.path.basename(file_path),
            "file_type": ext.lstrip("."),
            "num_tokens": len(tokens),
            "num_chunks": len(chunks),
        }

        if self.logger:
            self.logger.info(
                f"Archivo '{metadata['file_name']}' cargado: {metadata['num_tokens']} tokens en {metadata['num_chunks']} fragmentos"
            )

        return {"content": text, "chunks": chunks, "metadata": metadata}
