"""
Page Object para la navegación por el menú principal del CMS. Contiene
métodos para abrir cada módulo (CM) desde la vista de menú. Las rutas y
selectores utilizados aquí deben ser actualizados de acuerdo con los
data‑testids o textos visibles en la aplicación. Centralizar la
navegación evita duplicar la lógica de localización de elementos.
"""

from playwright.sync_api import Page, expect


class MenuPage:
    """Modela la navegación del menú principal del CMS."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def _open_menu_item(self, text: str) -> None:
        """
        Método genérico para abrir un elemento del menú usando el cuadro de búsqueda.
        Llena el input de búsqueda (por id), hace clic en el botón de buscar y espera el iframe del módulo.
        """
        # Llenar el input de búsqueda usando el id real
        self.page.fill("#Sbar", text)
        # Hacer clic en el botón de búsqueda
        self.page.click("button.searchB", force=True)
        # Esperar a que el iframe del módulo aparezca (si aplica)
        iframe_selector = f"iframe[name='iframe_{text.upper()}']"
        self.page.wait_for_selector(iframe_selector, timeout=30_000)

    def open_cm14(self) -> None:
        """Abre el módulo CM14 – Trazabilidad de Tarjetas."""
        self._open_menu_item("CM14" if self.page else "")

    def open_cm44(self) -> None:
        """Abre el módulo CM44 – Reimpresión de Solicitudes."""
        self._open_menu_item("CM44")

    def open_cm45(self) -> None:
        """Abre el módulo CM45 – Consulta de Tarjetas."""
        self._open_menu_item("CM45")

    def open_cm16(self) -> None:
        """Abre el módulo CM16 – Tarjeta por Cuenta."""
        self._open_menu_item("CM16")

    def open_cm18(self) -> None:
        """Abre el módulo CM18 – Tarjetas por Opción."""
        self._open_menu_item("CM18")

    def open_cm19(self) -> None:
        """Abre el módulo CM19 – Historial de Tarjetas."""
        self._open_menu_item("CM19")

    def open_cm21(self) -> None:
        """Abre el módulo CM21 – Consulta de Clave."""
        self._open_menu_item("CM21")

    def open_cm22(self) -> None:
        """Abre el módulo CM22 – Reporte de Tarjetas por Procesos."""
        self._open_menu_item("CM22")

    def open_cm46(self) -> None:
        """Abre el módulo CM46 – Reporte de Lotes Pendientes."""
        self._open_menu_item("CM46")

    def open_cm60(self) -> None:
        """Abre el módulo CM60 – Tarjetas Canceladas."""
        self._open_menu_item("CM60")

    def open_cm85(self) -> None:
        """Abre el módulo CM85 – Reporte de Tarjetas Emitidas."""
        self._open_menu_item("CM85")

    # Métodos adicionales para módulos sin automatización implementada
    def open_cm87(self) -> None:
        self._open_menu_item("CM87")

    def open_cma4(self) -> None:
        self._open_menu_item("CMA4")

    def open_cm88(self) -> None:
        self._open_menu_item("CM88")

    def open_cm17(self) -> None:
        self._open_menu_item("CM17")

    def open_cm89(self) -> None:
        self._open_menu_item("CM89")

    def open_cm97(self) -> None:
        self._open_menu_item("CM97")

    def open_md16(self) -> None:
        self._open_menu_item("MD16")