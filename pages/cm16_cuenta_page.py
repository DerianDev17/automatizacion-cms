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
        # esperar al iframe del módulo CM16
        self.page.wait_for_selector("iframe[name='iframe_CM16']", timeout=30_000)
        
    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM16']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM16")
        return frame
         

    def buscar_por_cuenta(self, cuenta: str) -> None:
        """Ingresa el número de cuenta y ejecuta la consulta."""
        # fallback a nivel de página si es necesario (no recomendado)
        self.page.fill("input[placeholder='Cuenta']", cuenta)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def buscar_por_cuenta_en_frame(self, cuenta: str, tipo_cuenta: str = "AH") -> None:
        """Realiza la búsqueda dentro del iframe: selecciona tipo y rellena cuenta."""
        frame = self._get_frame()
        frame.wait_for_selector("select#ctl00_maincontent_CboTipoCuenta", timeout=10_000)
        frame.locator("select#ctl00_maincontent_CboTipoCuenta").select_option(label=tipo_cuenta)
        frame.locator("input#ctl00_maincontent_TxtCuenta").fill(cuenta)

    def procesar_and_capture(self, cuenta: str, tipo_cuenta: str = "AH", screenshot_report: str = "screenshot_cm16_report.png") -> None:
        """Ejecuta la búsqueda en el iframe, pulsa Aceptar y captura el popup PDF."""
        frame = self._get_frame()
        # asegurar que selects/input estén rellenados
        self.buscar_por_cuenta_en_frame(cuenta, tipo_cuenta)

        # Click en Aceptar dentro del iframe y capturar popup
        with self.page.expect_popup() as popup_info:
            frame.get_by_role("button", name="Aceptar").click()
        report_page = popup_info.value
        report_page.wait_for_load_state("load")
        report_page.wait_for_timeout(1_000)
        try:
            report_page.screenshot(path=screenshot_report, full_page=True)
        except Exception:
            pass
        report_page.close()

        # volver al menú principal y asegurar que la pantalla principal esté visible
        self.page.bring_to_front()
        self.page.wait_for_selector("input[placeholder='Opción']", timeout=10_000)

    def validar_resultados(self, min_rows: int = 1) -> None:
        expect(self.page.locator("table tr")).to_have_count(at_least=min_rows)