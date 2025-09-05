"""
Page Object para el módulo **CM60 – Tarjetas Canceladas**. Permite
consultar las tarjetas canceladas dentro de un rango de fechas o por
criterio【547172095933312†L219-L220】.
"""

from playwright.sync_api import Page, expect


class CM60CanceladasPage:
    """Modela la pantalla CM60 – Tarjetas Canceladas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm60()
        expect(self.page.locator("text=CM60")).to_be_visible()

    def buscar(self, fecha_inicio: str, fecha_fin: str) -> None:
        """Busca tarjetas canceladas dentro de un rango de fechas (YYYY-MM-DD)."""
        # TODO: Implementar selección de fechas en el datepicker
        self.page.fill("input[name='fechaInicio']", fecha_inicio)
        self.page.fill("input[name='fechaFin']", fecha_fin)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)