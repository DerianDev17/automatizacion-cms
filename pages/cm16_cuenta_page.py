"""
Page Object para el módulo **CM16 – Tarjeta por Cuenta**. Permite
consultar las tarjetas asociadas a una cuenta bancaria específica【547172095933312†L214-L220】.
"""

from playwright.sync_api import Page, expect


class CM16CuentaPage:
    """Modela la pantalla CM16 – Tarjeta por Cuenta."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm16()
        expect(self.page.locator("iframe[name='iframe_CM16']")).to_be_visible()
         

    def buscar_por_cuenta(self, cuenta: str) -> None:
        """Ingresa el número de cuenta y ejecuta la consulta."""
        # TODO: Actualizar selectores
        self.page.fill("input[placeholder='Cuenta']", cuenta)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)