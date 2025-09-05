"""
Page Object para el módulo **CM46 – Reporte de Lotes Pendientes**. Permite
visualizar los lotes de tarjetas que están en proceso o pendientes de
procesamiento【547172095933312†L235-L239】.
"""

from playwright.sync_api import Page, expect


class CM46LotesPendientesPage:
    """Modela la pantalla CM46 – Reporte de Lotes Pendientes."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm46()
        expect(self.page.locator("text=CM46")).to_be_visible()

    def generar_reporte(self) -> None:
        """Genera el reporte de lotes pendientes."""
        self.page.click("button:has-text('Generar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def descargar_excel(self) -> None:
        """Descarga el reporte en formato Excel."""
        self.page.click("button:has-text('Exportar')")
        # TODO: Validar descarga y existencia del archivo