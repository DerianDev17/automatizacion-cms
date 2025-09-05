"""
Page Object para el módulo **CM14 – Trazabilidad de Tarjetas**.
Según la guía operativa, este módulo permite rastrear la historia de cada
tarjeta emitida, consultando eventos como emisión, renovación, reimpresión o
suspensión【547172095933312†L194-L204】. La automatización de este módulo
incluye la apertura desde el menú principal, la búsqueda de una tarjeta
mediante su número y la validación de que se presentan resultados en la
tabla.
"""

from playwright.sync_api import Page, expect


class CM14TrazabilidadPage:
    """Modela la pantalla CM14 – Trazabilidad de Tarjetas."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        """Utiliza el `MenuPage` para abrir este módulo."""
        menu_page.open_cm14()
        # Esperar a que el iframe de CM14 esté visible
        expect(self.page.locator("iframe[name='iframe_CM14']")).to_be_visible()

    def buscar_por_numero(self, numero_tarjeta: str) -> None:
        """Ingresa el número de tarjeta y dispara la búsqueda.

        Este método debe ajustar los selectores a la interfaz real del CMS:
        - Ubicar el campo de búsqueda (p. ej., placeholder 'Número de Tarjeta').
        - Ingresar el número y pulsar el botón de buscar/consultar.
        """
        # TODO: Actualizar con selectors específicos (data‑testid) una vez conocidos.
        self.page.fill("input[placeholder='Número de Tarjeta']", numero_tarjeta)
        self.page.click("button:has-text('Buscar')")
        # Esperar a que la tabla cargue (podría usarse un spinner o contador de filas)
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def validar_resultados(self, min_rows: int = 1) -> None:
        """Valida que la tabla de resultados contenga al menos `min_rows` filas."""
        rows = self.page.locator("table tr")
        expect(rows).to_have_count(at_least=min_rows)