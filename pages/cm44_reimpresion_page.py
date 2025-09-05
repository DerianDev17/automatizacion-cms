"""
Page Object para el módulo **CM44 – Reimpresión de Solicitudes**. Este
módulo permite consultar solicitudes de tarjetas y gestionar su
reimpresión【547172095933312†L194-L202】. La interacción típica
consiste en abrir el módulo desde el menú, filtrar por número de
solicitud o tarjeta y descargar el reporte.
"""

from playwright.sync_api import Page, expect


class CM44ReimpresionPage:
    """Modela la pantalla CM44 – Reimpresión de Solicitudes."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm44()
        expect(self.page.locator("text=CM44")).to_be_visible()

    def buscar_por_solicitud(self, numero_solicitud: str) -> None:
        """Busca una solicitud para reimpresión mediante su número."""
        # TODO: Ajustar selector al campo real
        self.page.fill("input[placeholder='Solicitud']", numero_solicitud)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def descargar_reporte(self) -> None:
        """Descarga el reporte generado (PDF/CSV). Requiere permisos."""
        # TODO: Implementar descarga real y validación de archivo
        self.page.click("button:has-text('Exportar')")