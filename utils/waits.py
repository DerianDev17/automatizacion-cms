"""
Funciones de espera personalizadas para pruebas Playwright.
Estas utilidades encapsulan patrones comunes de sincronización, por
ejemplo: esperar a que desaparezca un spinner de carga, a que se
descargue un archivo o a que se estabilice un conteo de filas en una tabla.
"""

from playwright.sync_api import Page, expect


def wait_for_spinner(page: Page, spinner_selector: str = "div.spinner") -> None:
    """Espera a que desaparezca un spinner en pantalla."""
    try:
        expect(page.locator(spinner_selector)).to_be_hidden(timeout=30000)
    except Exception:
        # Si el spinner no existe, se ignora
        pass


def wait_for_download(page: Page, trigger_action, timeout: int = 30000):
    """
    Espera a que se complete una descarga. La función `trigger_action` debe
    desencadenar la descarga (por ejemplo, hacer clic en 'Exportar'). Devuelve
    el objeto Download de Playwright.
    """
    with page.expect_download(timeout=timeout) as download_info:
        trigger_action()
    download = download_info.value
    return download