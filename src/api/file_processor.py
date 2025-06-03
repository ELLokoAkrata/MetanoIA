"""Procesamiento básico de archivos para MetanoIA."""

from typing import List
from src.utils.file_utils import split_text_by_tokens, summarize_text


class FileProcessor:
    """Clase para operaciones comunes sobre archivos de texto."""

    def __init__(self, max_tokens: int = 200):
        """Inicializa el procesador con un límite de tokens.

        Args:
            max_tokens: Número máximo de tokens por operación.
        """
        self.max_tokens = max_tokens

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
