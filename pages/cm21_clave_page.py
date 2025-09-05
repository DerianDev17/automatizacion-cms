"""
Page Object para el módulo **CM21 – Consulta de Clave**. Según la guía,
esta pantalla permite consultar la clave asociada a una tarjeta o
cliente【547172095933312†L214-L217】. El acceso a esta información suele
estar restringido, por lo que la automatización debe contemplar roles y
permisos adecuados.
"""

from playwright.sync_api import Page, expect


class CM21ClavePage:
    """Modela la pantalla CM21 – Consulta de Clave."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm21()
        expect(self.page.locator("text=CM21")).to_be_visible()

    def consultar_clave(self, identificador: str) -> None:
        """Realiza la consulta de la clave por identificador de tarjeta/cliente."""
        # TODO: Ajustar selectores
        self.page.fill("input[placeholder='Identificador']", identificador)
        self.page.click("button:has-text('Consultar')")
        expect(self.page.locator("text=Clave:")).to_be_visible()