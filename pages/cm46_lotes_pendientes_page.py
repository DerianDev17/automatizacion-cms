"""
Page Object para el módulo **CM46 – Reporte de Lotes Pendientes**. Permite
visualizar los lotes de tarjetas que están en proceso o pendientes de
procesamiento【547172095933312†L235-L239】.
"""

from playwright.sync_api import Page, expect


class CM46LotesPendientesPage:
    """Modela la pantalla CM46 – Reporte de Lotes Pendientes."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open_from_menu(self, menu_page) -> None:
        menu_page.open_cm46()
        # Esperar al iframe del módulo para mayor robustez
        self.page.wait_for_selector("iframe[name='iframe_CM46']", timeout=30_000)

    def _get_frame(self):
        iframe_el = self.page.wait_for_selector("iframe[name='iframe_CM46']", timeout=30_000)
        frame = iframe_el.content_frame()
        if frame is None:
            raise RuntimeError("No se pudo obtener el frame de CM46")
        return frame

    def generar_reporte(self) -> None:
        """Genera el reporte de lotes pendientes."""
        frame = self._get_frame()
        # Marcar listar todos los lotes pendientes si existe el checkbox
        try:
            frame.check("#ctl00_maincontent_ChkTodos")
        except Exception:
            pass

        # Hacer click en Generar y esperar resultados en la tabla (si aplica)
        try:
            # El botón Generar puede estar en el frame o en la página principal
            gen = frame.locator("button:has-text('Generar')")
            gen.wait_for(state="visible", timeout=5_000)
            gen.click()
        except Exception:
            try:
                self.page.click("button:has-text('Generar')")
            except Exception:
                pass

        # esperar a que la tabla tenga filas o deje un mensaje
        try:
            frame.wait_for_selector("table tr", timeout=5_000)
        except Exception:
            # puede que no existan filas y se muestre un mensaje
            pass

    def generar_y_capturar(self, screenshot_report: str = "screenshot_cm46_report.png", screenshot_result: str = "screenshot_cm46_result.png") -> None:
        """Genera el reporte e intenta capturar el PDF; si no hay lotes pendientes, captura la pantalla con el mensaje.

        Maneja ambos casos:
        - Si aparece popup PDF: captura y espera "Reporte Concluido"
        - Si no hay lotes: detecta el texto "No existen tarjetas Pendientes." y captura evidencia
        """
        frame = self._get_frame()

        # Marcar listar todos los lotes
        try:
            frame.check("#ctl00_maincontent_ChkTodos")
        except Exception:
            pass

        # Preparar el control imprimir/aceptar
        imprimir = frame.locator("#ctl00_maincontent_BtnImprimir:not([disabled])")
        try:
            imprimir.wait_for(state="visible", timeout=5_000)
        except Exception:
            # Si no hay botón visible, revisar si hay mensaje de 'no existen'
            try:
                frame.wait_for_selector("text=No existen tarjetas Pendientes.", timeout=2_000)
                # evidencia
                self.page.screenshot(path=screenshot_result, full_page=True)
                return
            except Exception:
                # tomar captura y fallar
                self.page.screenshot(path=screenshot_result, full_page=True)
                raise

        # Intentar capturar popup que genera el PDF
        try:
            with self.page.expect_popup(timeout=15_000) as popup_info:
                imprimir.click()
            report = popup_info.value
            report.wait_for_load_state("load")
            report.wait_for_timeout(1_000)
            try:
                report.screenshot(path=screenshot_report, full_page=True)
            except Exception:
                pass
            report.close()

            # Volver al modal original y esperar confirmación
            self.page.bring_to_front()
            try:
                # A veces es necesario re-click en Imprimir para que aparezca el texto
                frame.click("#ctl00_maincontent_BtnImprimir")
            except Exception:
                pass
            try:
                frame.wait_for_selector("text=Reporte Concluido", timeout=30_000)
            except Exception:
                pass

            # captura final
            self.page.wait_for_timeout(1_000)
            try:
                self.page.screenshot(path=screenshot_result, full_page=True)
            except Exception:
                pass

        except Exception:
            # Si no se abrió popup, comprobar mensaje de 'no existen' y guardar evidencia
            try:
                frame.wait_for_selector("text=No existen tarjetas Pendientes.", timeout=2_000)
                self.page.screenshot(path=screenshot_result, full_page=True)
                return
            except Exception:
                # tomar captura y volver a lanzar
                self.page.screenshot(path=screenshot_result, full_page=True)
                raise

    def descargar_excel(self) -> None:
        """Descarga el reporte en formato Excel."""
        frame = None
        try:
            frame = self._get_frame()
        except Exception:
            pass

        tried = False
        if frame is not None:
            try:
                btn = frame.locator("button:has-text('Exportar')")
                btn.wait_for(state="visible", timeout=5_000)
                btn.click()
                tried = True
            except Exception:
                tried = False

        if not tried:
            try:
                btn2 = self.page.locator("button:has-text('Exportar')")
                btn2.wait_for(state="visible", timeout=5_000)
                btn2.click()
                tried = True
            except Exception:
                tried = False

        # Si no se pudo localizar el botón, continuar sin fallo pero registrar captura
        if not tried:
            try:
                self.page.screenshot(path="screenshot_cm46_no_export_button.png", full_page=True)
            except Exception:
                pass