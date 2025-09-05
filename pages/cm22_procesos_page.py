"""
Page Object para el módulo **CM22 – Reporte de Tarjetas por Procesos**. Este
reporte agrupa las tarjetas por el proceso que las generó (emisión,
renovación, reposición, etc.)【547172095933312†L221-L224】.
"""

from playwright.sync_api import Page, expect


class CM22ProcesosPage:
    """Modela la pantalla CM22 – Reporte de Tarjetas por Procesos."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm22()
        expect(self.page.locator("text=CM22")).to_be_visible()

    def seleccionar_proceso(self, proceso: str) -> None:
        """Selecciona el proceso sobre el cual generar el reporte."""
        self.page.select_option("select[name='proceso']", label=proceso)

    def generar_reporte(self) -> None:
        self.page.click("button:has-text('Generar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)