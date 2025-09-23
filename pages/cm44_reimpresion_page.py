"""
Page Object para el módulo **CM44 – Reimpresión de Solicitudes**. Este
módulo permite consultar solicitudes de tarjetas y gestionar su
reimpresión【547172095933312†L194-L202】. La interacción típica
consiste en abrir el módulo desde el menú, filtrar por número de
solicitud o tarjeta y descargar el reporte.
"""

from playwright.sync_api import Page, expect


class CM44ReimpresionPage:
    """Modela la pantalla CM44 – Reimpresión de Solicitudes."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm44()
        # El botón de texto puede estar oculto; esperar directamente al iframe del módulo
        self.page.wait_for_selector("iframe[name='iframe_CM44']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM44']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM44")
        return frame

    def buscar_por_solicitud(self, numero_solicitud: str) -> None:
        """Busca una solicitud para reimpresión mediante su número."""
        # TODO: Ajustar selector al campo real
        self.page.fill("input[placeholder='Solicitud']", numero_solicitud)
        self.page.click("button:has-text('Buscar')")
        expect(self.page.locator("table tr")).to_have_count(at_least=1)

    def buscar_por_tarjeta(self, card_number: str) -> None:
        """Busca una solicitud por número de tarjeta dentro del iframe y espera el postback."""
        frame = self._get_frame()
        frame.fill("#ctl00_maincontent_TxtTarjeta", card_number)
        frame.evaluate("__doPostBack('ctl00$maincontent$TxtTarjeta','');")
        frame.wait_for_selector("#ctl00_maincontent_TxtTarjeta[value*='XXXX']", timeout=10_000)

    def descargar_reporte(self, screenshot_confirmation: str = "screenshot_cm44_confirmation.png", screenshot_report: str = "screenshot_cm44_report.png") -> None:
        """Realiza el flujo de selección e impresión dentro del iframe y captura popup/report y confirmación."""
        frame = self._get_frame()

        # Continuar
        cont = frame.locator("#ctl00_maincontent_BtnContinuar:not([disabled])")
        cont.wait_for(state="visible", timeout=15_000)
        cont.click()
        frame.wait_for_timeout(1_000)

        # Seleccionar tipo de documento
        try:
            frame.select_option("#ctl00_maincontent_CboTipoDoc", label="Solicitud Tarjeta")
        except Exception:
            pass

        # Preparar imprimir
        imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        imprimir.wait_for(state="visible", timeout=15_000)

        # Capturar popup al hacer clic
        with self.page.expect_popup() as popup_info:
            imprimir.click()
        popup = popup_info.value

        # Esperar y verificar el mensaje de confirmación en la vista principal
        frame.wait_for_selector("text=Impresion se realizo Correctamente", timeout=30_000)
        self.page.wait_for_timeout(1_000)
        self.page.screenshot(path=screenshot_confirmation, full_page=True)

        # Esperar a que el PDF cargue y tomar screenshot
        popup.wait_for_load_state("load")
        popup.wait_for_timeout(1_000)
        try:
            popup.screenshot(path=screenshot_report, full_page=True)
        except Exception:
            pass

        # Regresar al menú (traer al frente)
        self.page.bring_to_front()

    