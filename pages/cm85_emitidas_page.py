"""
Page Object para el módulo **CM85 – Reporte de Tarjetas Emitidas**. Este
reporte lista las tarjetas emitidas en un periodo de tiempo y permite
exportar la información【547172095933312†L211-L213】.
"""

from playwright.sync_api import Page, expect


class CM85EmitidasPage:
    """Modela la pantalla CM85 – Reporte de Tarjetas Emitidas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm85()
        expect(self.page.locator("text=CM85")).to_be_visible()

    def buscar(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Filtra las tarjetas emitidas entre las fechas indicadas."""
        # TODO: Actualizar selectors para datepicker
        self.page.fill("input[name='fechaInicio']", fecha_inicio)
        self.page.fill("input[name='fechaFin']", fecha_fin)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def exportar_excel(self) -> None:
        """Exporta el reporte generado a Excel."""
        self.page.click("button:has-text('Exportar')")
        # TODO: Validar existencia del archivo descargado