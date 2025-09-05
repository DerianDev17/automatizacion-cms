"""
Page Object para el módulo **CM18 – Tarjetas por Opción**. Este reporte
clasifica las tarjetas según una opción o criterio seleccionado por el
usuario【547172095933312†L194-L203】.
"""

from playwright.sync_api import Page, expect


class CM18OpcionPage:
    """Modela la pantalla CM18 – Tarjetas por Opción."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm18()
        expect(self.page.locator("text=CM18")).to_be_visible()

    def seleccionar_opcion(self, opcion: str) -> None:
        """Selecciona la opción deseada en un combo o lista desplegable."""
        # TODO: Implementar selección real
        self.page.select_option("select[name='opcion']", label=opcion)

    def generar_reporte(self) -> None:
        """Genera el reporte tras seleccionar la opción."""
        self.page.click("button:has-text('Generar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)