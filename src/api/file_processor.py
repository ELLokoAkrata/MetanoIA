"""Procesamiento básico de archivos para MetanoIA."""

from typing import List, Dict, Any
from src.utils.file_utils import (
    split_text_by_tokens,
    summarize_text,
    read_pdf,
    read_text,
    read_json,
)


class FileProcessor:
    """Clase para operaciones comunes sobre archivos de texto y datos."""

    def __init__(self, max_tokens: int = 200, logger=None):
        """Inicializa el procesador con un límite de tokens.

        Args:
            max_tokens: Número máximo de tokens por operación.
            logger: Instancia opcional para registrar eventos.
        """
        self.max_tokens = max_tokens
        self.logger = logger

    def dividir_en_fragmentos(self, texto: str) -> List[str]:
        """Divide un texto largo en fragmentos manejables.

        Args:
            texto: Texto a dividir.

        Returns:
            Lista de fragmentos que no superan ``self.max_tokens`` tokens.
        """
        return split_text_by_tokens(texto, self.max_tokens)

    def resumir(self, texto: str) -> str:
        """Genera un resumen simple del texto si es demasiado extenso.

        Args:
            texto: Texto a resumir.

        Returns:
            Texto original o resumido según el límite establecido.
        """
        return summarize_text(texto, self.max_tokens)

    def leer_pdf(self, data: bytes) -> str:
        """Extrae texto de un archivo PDF."""

        text = read_pdf(data)
        if self.logger:
            self.logger.info("PDF procesado")
        return self.resumir(text)

    def leer_txt(self, data: bytes | str) -> str:
        """Procesa un archivo de texto."""

        text = read_text(data)
        if self.logger:
            self.logger.info("Archivo TXT procesado")
        return self.resumir(text)

    def leer_json(self, data: bytes | str) -> Dict[str, Any]:
        """Procesa un archivo JSON y devuelve el diccionario correspondiente."""

        obj = read_json(data)
        if self.logger:
            self.logger.info("Archivo JSON procesado")
        return obj

    def process_file(self, data: bytes | str, file_type: str) -> Dict[str, Any]:
        """Procesa un archivo según su tipo."""

        try:
            if file_type == "pdf":
                content = self.leer_pdf(data)
            elif file_type == "txt":
                content = self.leer_txt(data)
            elif file_type == "json":
                content = self.leer_json(data)
            else:
                return {"success": False, "error": "Tipo de archivo no soportado"}

            return {"success": True, "content": content, "file_type": file_type}

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error al procesar archivo {file_type}: {e}")
            return {"success": False, "error": str(e)}
