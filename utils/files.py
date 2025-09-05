"""
Utilidades para gestionar descargas y archivos generados durante las pruebas.
Playwright permite interceptar objetos `Download` y guardar el archivo
directamente. Además, este módulo puede ofrecer funciones para limpiar
directorios temporales antes de ejecutar pruebas.
"""

import os
from pathlib import Path
from playwright.sync_api import Download


def save_download(download: Download, directory: str = "downloads") -> Path:
    """
    Guarda un objeto `Download` de Playwright en el directorio indicado y
    devuelve la ruta del archivo guardado.
    """
    os.makedirs(directory, exist_ok=True)
    # Si download.suggested_filename no existe, usa un nombre genérico
    filename = download.suggested_filename or "archivo_descargado"
    filepath = Path(directory) / filename
    download.save_as(str(filepath))
    return filepath