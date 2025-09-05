"""
Page Object para el módulo **CM45 – Consulta de Tarjetas**. Permite
consultar el estado de las tarjetas emitidas, suspendidas o canceladas
mediante diferentes filtros (número de tarjeta, cliente, fecha, etc.)【547172095933312†L194-L202】.
"""

from playwright.sync_api import Page, expect


class CM45ConsultaPage:
    """Modela la pantalla CM45 – Consulta de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm45()
        expect(self.page.locator("text=CM45")).to_be_visible()

    def buscar(self, criterio: str, valor: str) -> None:
        """Realiza una búsqueda por un criterio específico.

        Por ejemplo:
        - criterio='tarjeta', valor='5353…1234'
        - criterio='cliente', valor='Cédula/Nombre'
        """
        # TODO: Implementar selección de criterio y campo dinámico
        selector_campo = f"input[placeholder='{criterio}']"
        self.page.fill(selector_campo, valor)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)