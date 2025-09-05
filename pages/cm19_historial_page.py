"""
Page Object para el módulo **CM19 – Historial de Tarjetas**. Permite
consultar el historial de transacciones o estados de una tarjeta a lo
largo del tiempo【547172095933312†L204-L208】.
"""

from playwright.sync_api import Page, expect


class CM19HistorialPage:
    """Modela la pantalla CM19 – Historial de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm19()
        expect(self.page.locator("text=CM19")).to_be_visible()

    def buscar_por_numero(self, numero_tarjeta: str) -> None:
        """Ingresa el número de tarjeta y busca su historial."""
        # TODO: Actualizar selectores
        self.page.fill("input[placeholder='Número de Tarjeta']", numero_tarjeta)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)