"""
Clases placeholder para los módulos del CMS que aún no tienen
automatización implementada. Se basan en la lista de módulos de la guía
operativa【547172095933312†L194-L241】 y sirven como punto de partida para
futuras implementaciones. Cada clase incluye un método `open_from_menu` y
documentación breve sobre el propósito del módulo.
"""

from playwright.sync_api import Page, expect


class BasePlaceholderPage:
    """Clase base para placeholders, proporciona un método genérico de navegación."""

    module_code: str = ""
    description: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        """Abre el módulo a través del menú utilizando el código CM/MD."""
        getattr(menu_page, f"open_{self.module_code.lower()}")()
        expect(self.page.locator(f"text={self.module_code.upper()}"))\
            .to_be_visible()

    def not_implemented(self) -> None:
        raise NotImplementedError(
            f"La automatización de {self.module_code} ({self.description}) aún no está implementada."
        )


class CM87HistoriaOficinaPage(BasePlaceholderPage):
    module_code = "cm87"
    description = "Historia de Tarjetas por Oficina"


class CMA4EmitidasProductoPage(BasePlaceholderPage):
    module_code = "cma4"
    description = "Tarjetas Emitidas por Producto"


class CM88AnuladasSuspendidasPage(BasePlaceholderPage):
    module_code = "cm88"
    description = "Reporte de Tarjetas Anuladas, Suspendidas, Bloqueadas"


class CM17CostosPage(BasePlaceholderPage):
    module_code = "cm17"
    description = "Reporte de Costos"


class CM89VencerPage(BasePlaceholderPage):
    module_code = "cm89"
    description = "Reporte de Tarjetas por Vencer"


class CM97BinPage(BasePlaceholderPage):
    module_code = "cm97"
    description = "Reporte de Tarjetas por BIN"


class MD16AutorizacionesPage(BasePlaceholderPage):
    module_code = "md16"
    description = "Reporte de Autorización de Transacciones"